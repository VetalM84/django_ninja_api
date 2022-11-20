"""API routes."""

from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.pagination import paginate

from currency.models import Currency, Offer
from currency.schemas import CurrencyBase, ErrorMsg, OfferIn, CurrencyIn

api = NinjaAPI()


@api.get("/", tags=["Server status"])
def server_status(request):
    """Check server health status."""
    return {"Server": "running..."}


@api.get(
    "/currency/all/",
    response={200: List[CurrencyBase], 404: ErrorMsg},
    tags=["Currency"],
)
@paginate()
def get_currencies(request):
    """Get all currencies."""
    currency_list = Currency.objects.all()
    if len(currency_list) == 0:
        return 404, {"message": "Nothing found"}
    # currency_list = Currency.objects.annotate(offers_count=Count("currencies_to_sell"))
    return currency_list


@api.post("/currency/", response={201: CurrencyBase, 400: ErrorMsg}, tags=["Currency"])
def add_currency(request, payload: CurrencyIn):
    """Add new currency."""
    currency = Currency.objects.filter(code__iexact=payload.code)
    if len(currency) > 0:
        return 400, {"message": "Currency with that code already exists"}
    # currency.create(**payload.dict())
    return 201, currency.create(**payload.dict())


@api.delete("/currency/{currency_id}", tags=["Currency"])
def delete_currency(request, currency_id: int):
    """Delete currency."""
    currency = get_object_or_404(Currency, pk=currency_id)
    currency.delete()
    return {"success": True}


@api.post("/offer/", tags=["Offer"])
def add_offer(request, payload: OfferIn):
    """Add new offer."""
    offer = Offer.objects.create(**payload.dict())
    return {"id": offer.pk}


@api.delete("/offer/{offer_id}", tags=["Offer"])
def delete_offer(request, offer_id: int):
    """Delete offer."""
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.delete()
    return {"success": True}