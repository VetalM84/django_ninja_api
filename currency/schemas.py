"""Data serialization for API."""

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


class OfferIn(Schema):
    """Offer schema for POST method."""
    currency_to_sell_id: int
    currency_to_buy_id: int
    user_id: int
    amount: float
    exchange_rate: float


class ErrorMsg(Schema):
    """Base schema for error message response."""
    message: str
