"""API routes."""
from typing import List

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.pagination import paginate

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

api = NinjaAPI()


@api.get("/", tags=["Server status"])
def server_status(request):
    """Check server health status."""
    return {"Server": "running..."}


@api.get("/currencies/{currency_id}", response=CurrencyBase, tags=["Currency"])
def get_single_currency(request, currency_id: int):
    """Get single currency."""
    return get_object_or_404(Currency, pk=currency_id)


@api.get("/currencies", response=List[CurrencyBase], tags=["Currency"])
@paginate()
def get_all_currencies(request):
    """Get all currencies."""
    # currency_list = Currency.objects.annotate(offers_count=Count("currencies_to_sell"))
    return Currency.objects.all()


@api.post("/currencies", response={201: CurrencyBase, 400: ErrorMsg}, tags=["Currency"])
def add_new_currency(request, payload: CurrencyIn):
    """Add new currency."""
    if Currency.objects.filter(code__iexact=payload.code).exists():
        return 400, {"message": "Currency with that code already exists"}
    return 201, Currency.objects.create(**payload.dict())


@api.put("/currencies/{currency_id}", response={200: CurrencyBase}, tags=["Currency"])
def edit_currency(request, currency_id: int, payload: CurrencyIn):
    """Edit currency."""
    currency = get_object_or_404(Currency, pk=currency_id)
    for attr, value in payload.dict().items():
        setattr(currency, attr, value)
    currency.save()
    return 200, currency


@api.delete(
    "/currencies/{currency_id}", response={204: None, 400: ErrorMsg}, tags=["Currency"]
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
    return get_object_or_404(Offer, pk=offer_id)


@api.get("/offers", response=List[OfferBase], tags=["Offer"])
@paginate()
def get_all_active_offers(request):
    """Get all offers with pagination."""
    return Offer.objects.filter(active_state=True)


@api.get("/users/{user_id}/offers", response=List[OfferBase], tags=["Offer", "User"])
@paginate()
def get_user_offers(request, user_id):
    """Get all user offers with pagination."""
    return Offer.objects.filter(seller_id=user_id)


@api.get(
    "/currencies/{currency_to_sell_id}/offers",
    response=List[OfferBase],
    tags=["Offer", "Currency"],
)
@paginate()
def get_all_offers_by_sell_currency(request, currency_to_sell_id):
    """Get all offers by sell currency with pagination."""
    return Offer.objects.filter(currency_to_sell_id=currency_to_sell_id)


@api.post("/offers", response={201: OfferBase}, tags=["Offer"])
def add_new_offer(request, payload: OfferIn):
    """Add new offer."""
    return 201, Offer.objects.create(**payload.dict())


@api.patch(
    "/offers/{offer_id}",
    response=OfferBase,
    tags=["Offer"],
    exclude_unset=True,
)
def toggle_offer_state(request, offer_id, payload: OfferState):
    """Toggle offer state (enable/disable)."""
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.active_state = payload.active_state
    offer.save()
    return offer


@api.delete("/offers/{offer_id}", response={204: None, 400: ErrorMsg}, tags=["Offer"])
def delete_offer(request, offer_id: int):
    """Delete offer."""
    try:
        offer = get_object_or_404(Offer, pk=offer_id)
        offer.delete()
        return 204, None
    except ProtectedError:
        return 400, {"message": "You can't delete an offer having any deal"}


@api.get("/users/{user_id}", response=UserExtraDataOut, tags=["User"])
def get_user_info(request, user_id):
    """Get user profile information with offers and deals."""
    return get_object_or_404(User, pk=user_id)


@api.get("/deals/{deal_id}", response=DealExtraDataOut, tags=["Deal"])
def get_single_deal(request, deal_id):
    """Get single deal."""
    deal = get_object_or_404(Deal, pk=deal_id)
    return deal


@api.get("/deals", response=List[DealBase], tags=["Deal"])
def get_all_deals(request):
    return Deal.objects.all()


@api.post("/deals", response={201: DealBase, 400: ErrorMsg}, tags=["Deal"])
def add_new_deal(request, payload: DealIn):
    """Add new deal."""
    offer = get_object_or_404(Offer, pk=payload.offer_id)
    if not offer.active_state or offer.seller.pk == payload.buyer_id:
        return 400, {"message": "You can't make a deal to this offer"}
    try:
        deal = Deal.objects.create(**payload.dict())
        return 201, deal
    except IntegrityError:
        return 400, {"message": "You can't make a deal to this offer"}
