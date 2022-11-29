"""API routes."""
import datetime
from datetime import timezone
from decimal import Decimal
from typing import List

import jwt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from ninja import Form, NinjaAPI
from ninja.errors import ValidationError
from ninja.pagination import paginate
from ninja.security import HttpBearer

from currency.models import Currency, Deal, Offer
from currency.schemas import (
    CurrencyBase,
    CurrencyIn,
    DealBase,
    DealExtraDataOut,
    DealIn,
    ErrorMsg,
    OfferBase,
    OfferIn,
    OfferState,
    OfferWithDealOut,
    UserExtraDataOut,
)
from django_ninja_api import settings

api = NinjaAPI()


def create_token(username):
    """Create JWT method."""
    jwt_signing_key = getattr(settings, "JWT_SIGNING_KEY", None)
    jwt_access_expire = getattr(settings, "JWT_ACCESS_EXPIRY", 60)
    payload = {"username": username}
    access_expire = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
        minutes=jwt_access_expire
    )
    payload.update({"exp": access_expire})
    token = jwt.encode(payload=payload, key=jwt_signing_key, algorithm="HS256")
    return token


class AuthBearer(HttpBearer):
    """Bearer auth type. Headers:
    Authorization: Bearer {token}
    """

    def authenticate(self, request, token):
        """Decode token to check its validity."""
        jwt_signing_key = getattr(settings, "JWT_SIGNING_KEY", None)
        try:
            payload = jwt.decode(token, key=jwt_signing_key, algorithms=["HS256"])
        except Exception as e:
            return {"error": e}
        username: str = payload.get("username", None)
        return username


@api.post("/sign_in", auth=None)
def sign_in(request, username: str = Form(...), password: str = Form(...)):
    """Obtain a token for further auth."""
    user_model = get_object_or_404(User, username=username)

    passwords_match = check_password(password, user_model.password)
    if not passwords_match:
        raise ValidationError([{"error": "Wrong password"}])

    token = create_token(user_model.username)
    return {"token": token}


@api.get("/", tags=["Server status"])
def server_status(request):
    """Check server health status."""
    return {"Server": "running..."}


@api.get("/currencies/{currency_id}", response=CurrencyBase, tags=["Currency"])
def get_single_currency(request, currency_id: int):
    """Get single currency."""
    currency = get_object_or_404(Currency, pk=currency_id)
    return currency


@api.get("/currencies", response=List[CurrencyBase], tags=["Currency"])
@paginate()
def get_all_currencies(request):
    """Get all currencies."""
    # currency_list = Currency.objects.annotate(offers_count=Count("currencies_to_sell"))
    currencies = Currency.objects.all()
    return currencies


@api.post(
    "/currencies",
    response={201: CurrencyBase, 400: ErrorMsg},
    tags=["Currency"],
    auth=AuthBearer(),
)
def add_new_currency(request, payload: CurrencyIn):
    """Add new currency."""
    if Currency.objects.filter(code__iexact=payload.code).exists():
        return 400, {"message": "Currency with that code already exists"}
    currency = Currency.objects.create(**payload.dict())
    return 201, currency


@api.put(
    "/currencies/{currency_id}",
    response={200: CurrencyBase},
    tags=["Currency"],
    auth=AuthBearer(),
)
def edit_currency(request, currency_id: int, payload: CurrencyIn):
    """Edit currency."""
    currency = get_object_or_404(Currency, pk=currency_id)
    for attr, value in payload.dict().items():
        setattr(currency, attr, value)
    currency.save()
    return 200, currency


@api.delete(
    "/currencies/{currency_id}",
    response={204: None, 400: ErrorMsg},
    tags=["Currency"],
    auth=AuthBearer(),
)
def delete_currency(request, currency_id: int):
    """Delete currency."""
    try:
        get_object_or_404(Currency, pk=currency_id).delete()
        return 204, None
    except ProtectedError:
        return 400, {"message": "You can't delete currency having any offer."}


@api.get("/offers/{offer_id}", response=OfferWithDealOut, tags=["Offer"])
def get_single_offer(request, offer_id: int):
    """Get single offer with corresponding deal if any."""
    offer = get_object_or_404(Offer, pk=offer_id)
    return offer


@api.get("/offers", response=List[OfferBase], tags=["Offer"])
@paginate()
def get_all_active_offers(request):
    """Get all offers with pagination."""
    offers = Offer.objects.filter(active_state=True)
    return offers


@api.get(
    "/users/{user_id}/offers",
    response=List[OfferBase],
    tags=["Offer", "User"],
    auth=AuthBearer(),
)
@paginate()
def get_user_offers(request, user_id):
    """Get all user offers with pagination."""
    offers = Offer.objects.filter(seller_id=user_id)
    return offers


@api.get(
    "/currencies/{currency_to_sell_id}/offers",
    response=List[OfferBase],
    tags=["Offer", "Currency"],
)
@paginate()
def get_all_offers_by_sell_currency(request, currency_to_sell_id):
    """Get all offers by sell currency with pagination."""
    offers = Offer.objects.filter(currency_to_sell_id=currency_to_sell_id)
    return offers


@api.post("/offers", response={201: OfferBase}, tags=["Offer"], auth=AuthBearer())
def add_new_offer(request, payload: OfferIn):
    """Add new offer."""
    offer = Offer.objects.create(**payload.dict())
    return 201, offer


@api.patch(
    "/offers/{offer_id}",
    response=OfferBase,
    tags=["Offer"],
    exclude_unset=True,
    auth=AuthBearer(),
)
def toggle_offer_state(request, offer_id, payload: OfferState):
    """Toggle offer state (enable/disable)."""
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.active_state = payload.active_state
    offer.save()
    return offer


@api.delete(
    "/offers/{offer_id}",
    response={204: None, 400: ErrorMsg},
    tags=["Offer"],
    auth=AuthBearer(),
)
def delete_offer(request, offer_id: int):
    """Delete offer."""
    try:
        offer = get_object_or_404(Offer, pk=offer_id)
        offer.delete()
        return 204, None
    except ProtectedError:
        return 400, {"message": "You can't delete an offer having any deal"}


@api.get(
    "/users/{user_id}", response=UserExtraDataOut, tags=["User"], auth=AuthBearer()
)
def get_user_info(request, user_id):
    """Get user profile information with offers and deals."""
    user = get_object_or_404(User, pk=user_id)
    return user


@api.get("/deals/{deal_id}", response=DealExtraDataOut, tags=["Deal"])
def get_single_deal(request, deal_id):
    """Get single deal."""
    deal = get_object_or_404(Deal, pk=deal_id)
    return deal


@api.get("/deals", response=List[DealBase], tags=["Deal"])
def get_all_deals(request):
    deals = Deal.objects.all()
    return deals


@api.post(
    "/deals", response={201: DealBase, 400: ErrorMsg}, tags=["Deal"], auth=AuthBearer()
)
def add_new_deal(request, payload: DealIn):
    """Add new deal."""
    offer = get_object_or_404(Offer, pk=payload.offer_id)
    if (
        not offer.active_state
        or offer.seller.pk == payload.buyer_id
        or offer.amount < payload.amount
    ):
        return 400, {"message": "You can't make a deal to this offer"}
    offer.amount -= Decimal(payload.amount)
    offer.save()
    deal = Deal.objects.create(**payload.dict())
    return 201, deal
