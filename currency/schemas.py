"""Data serialization for API."""

from datetime import datetime
from typing import List

from ninja import ModelSchema, Schema

from currency.models import Currency, Deal, Offer, User

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


class OfferState(Schema):
    """Offer state for POST method to enable/disable an offer."""

    active_state: bool


class UserBase(Schema):
    """Base user schema for GET method."""

    id: int
    username = str
    first_name = str
    last_name = str
    email = str


class UserModel(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "username", "first_name", "last_name", "email"]


class UserDataOut(UserBase):
    """Extended user schema with extra data response."""

    offers: List[OfferBase]
    # TODO add Deals
    # deals: List[DealBase]


class ErrorMsg(Schema):
    """Base schema for error message response."""

    message: str
