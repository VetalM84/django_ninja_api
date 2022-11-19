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
async def get_currencies(request):
    """Get all currencies."""
    currency_list = [
        item
        async for item in Currency.objects.annotate(
            offers_count=Count("currencies_to_sell")
        )
    ]
    return currency_list


@api.post("/offer/", tags=["Offer"])
async def add_offer(request, payload: OfferIn):

    # currency_to_sell = await Currency.objects.aget(id=payload.currency_to_sell)
    # currency_to_buy = await Currency.objects.aget(id=payload.currency_to_buy)
    # user = await User.objects.aget(id=payload.user)
    # payload.currency_to_sell = currency_to_sell
    # payload.currency_to_buy = currency_to_buy
    # payload.user = user
    # print(payload)
    offer = await Offer.objects.acreate(**payload.dict())
    return {"id": offer.pk}


@api.delete("/currency/{currency_id}", tags=["Currency"])
async def delete_currency(request, currency_id: int):
    """Delete currency."""
    currency = await sync_to_async(get_object_or_404)(Currency, pk=currency_id)
    await currency.adelete()
    return {"success": True}


@api.delete("/offer/{offer_id}", tags=["Offer"])
async def delete_offer(request, offer_id: int):
    """Delete offer."""
    offer = await sync_to_async(get_object_or_404)(Offer, pk=offer_id)
    await sync_to_async(offer.delete)()
    return {"success": True}
