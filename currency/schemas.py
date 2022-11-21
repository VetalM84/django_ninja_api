"""Data serialization for API."""

from datetime import datetime

from ninja import ModelSchema, Schema

from currency.models import Currency, Deal, Offer

# class CurrenciesOut(ModelSchema):
#     class Config:
#         model = Currency
#         model_fields = ["id", "code", "name", "image"]


class CurrencyBase(Schema):
    """Base currency schema for GET method, response."""

    id: int
    code: str
    name: str
    image: str


class CurrencyIn(CurrencyBase):
    """Currency schema for POST method."""

    id: int = None


class OfferBase(Schema):
    """Base offer schema for GET method, response."""

    id: int
    currency_to_sell_id: int
    currency_to_buy_id: int
    amount: float
    exchange_rate: float
    user_id: int
    added_time: datetime = None
    active_state: bool = True


class OfferIn(OfferBase):
    """Offer schema for POST method."""

    id: int = None


class OfferState(OfferBase):
    """Offer state for POST method to enable/disable an offer."""

    active_state: bool


class ErrorMsg(Schema):
    """Base schema for error message response."""

    message: str
