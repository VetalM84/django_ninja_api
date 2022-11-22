"""Data serialization for API."""

from datetime import datetime
from typing import List

from ninja import Schema


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


class DealBase(Schema):
    """Base deal schema for GET method."""

    id: int
    seller_id: int
    buyer_id: int
    offer_id: int
    deal_time: datetime = None


class UserBase(Schema):
    """Base user schema for GET method."""

    id: int
    username: str
    first_name: str
    last_name: str
    email: str


class DealExtraDataOut(Schema):
    """Extended user schema with extra data response."""

    sold: List[DealBase]
    bought: List[DealBase]


class UserExtraDataOut(UserBase):
    """Extended user schema with extra data response."""

    offers: List[OfferBase]
    deals: DealExtraDataOut


class ErrorMsg(Schema):
    """Base schema for error message response."""

    message: str
