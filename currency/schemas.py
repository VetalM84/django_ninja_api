"""Data serialization for API."""

from ninja import ModelSchema, Schema

from currency.models import Currency, Offer


class CurrenciesOut(ModelSchema):
    class Config:
        model = Currency
        model_fields = ["id", "code", "country", "image"]


class OfferIn(Schema):
    currency_to_sell_id: int
    currency_to_buy_id: int
    user_id: int
    amount: float
    exchange_rate: float


# class OfferIn(ModelSchema):
#     class Config:
#         model = Offer
#         model_fields = [
#             "currency_to_sell",
#             "currency_to_buy",
#             "user",
#             "amount",
#             "exchange_rate",
#         ]
