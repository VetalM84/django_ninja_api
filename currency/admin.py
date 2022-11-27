from django.contrib import admin

from currency.models import Currency, Deal, Offer


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Currency model views on backend."""

    list_display = ("id", "code", "name")
    list_display_links = ("id", "code", "name")
    ordering = ("code",)
    search_fields = ("code", "name")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Offer model views on backend."""

    list_display = (
        "id",
        "currency_to_sell",
        "currency_to_buy",
        "amount",
        "exchange_rate",
        "seller",
        "added_time",
        "active_state",
    )
    list_display_links = ("id", "currency_to_sell", "currency_to_buy")
    ordering = ("id", "currency_to_sell", "currency_to_buy", "amount", "exchange_rate")
    search_fields = ("currency_to_sell", "currency_to_buy")
    list_filter = ("active_state",)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Deal model views on backend."""

    list_display = (
        "id",
        "seller",
        "buyer",
        "offer",
        "deal_time",
    )
    list_display_links = ("id", "seller", "buyer", "offer", "deal_time")
    ordering = ("deal_time",)
    search_fields = ("seller", "buyer")
