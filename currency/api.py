"""API routes."""

from typing import List

from asgiref.sync import sync_to_async
from django.db.models import Count
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from currency.models import Currency, Offer
from currency.schemas import CurrenciesOut, OfferIn

api = NinjaAPI()


@api.get("/")
def hello(request):
    return {"Server": "running..."}


@api.get("/currency/", response=List[CurrenciesOut], tags=["Currency"])
def get_currencies(request):
    """Get all currencies."""
    currency_list = Currency.objects.annotate(offers_count=Count("currencies_to_sell"))
    return currency_list


@api.post("/offer/", tags=["Offer"])
def add_offer(request, payload: OfferIn):

    # currency_to_sell = Currency.objects.get(id=payload.currency_to_sell)
    # currency_to_buy = Currency.objects.get(id=payload.currency_to_buy)
    # user = User.objects.get(id=payload.user)
    # payload.currency_to_sell = currency_to_sell
    # payload.currency_to_buy = currency_to_buy
    # payload.user = user
    # print(payload)
    offer = Offer.objects.create(**payload.dict())
    return {"id": offer.pk}


@api.delete("/currency/{currency_id}", tags=["Currency"])
def delete_currency(request, currency_id: int):
    """Delete currency."""
    currency = get_object_or_404(Currency, pk=currency_id)
    currency.delete()
    return {"success": True}


@api.delete("/offer/{offer_id}", tags=["Offer"])
def delete_offer(request, offer_id: int):
    """Delete offer."""
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.delete()
    return {"success": True}
