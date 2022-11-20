"""Currency app's DB models."""

from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    """Currency model."""

    code = models.CharField(
        max_length=3, unique=True, blank=False, null=False, verbose_name="Code"
    )
    name = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Name"
    )
    image = models.ImageField(verbose_name="Image")

    def __str__(self):
        """String representation of the object."""
        return self.code

    def save(self, *args, **kwargs):
        """Transform currency code to uppercase on save."""
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    class Meta:
        """Meta properties."""

        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class Offer(models.Model):
    """Sell currency offer model."""

    currency_to_sell = models.ForeignKey(
        to="Currency",
        on_delete=models.CASCADE,
        related_name="currencies_to_sell",
        verbose_name="Currency to sell",
    )
    currency_to_buy = models.ForeignKey(
        to="Currency",
        on_delete=models.CASCADE,
        related_name="currencies_to_buy",
        verbose_name="Currency to buy",
    )
    amount = models.DecimalField(
        decimal_places=2, max_digits=11, blank=False, null=False, verbose_name="Amount"
    )
    exchange_rate = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        blank=False,
        null=False,
        verbose_name="Exchange rate",
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="offers", verbose_name="User"
    )
    added_time = models.DateTimeField(auto_now=True, verbose_name="Added")
    active_state = models.BooleanField(default=True, verbose_name="Active state")

    def __str__(self):
        """String representation of the object."""
        return (
            self.currency_to_sell.code
            + " -> "
            + self.currency_to_buy.code
            + ": "
            + str(self.exchange_rate)
        )

    def disable_offer(self):
        """Disable offer upon deal."""
        self.state = False

    class Meta:
        """Meta properties."""

        verbose_name = "Offer"
        verbose_name_plural = "Offers"


class Deal(models.Model):
    """Deal model."""

    seller = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name="", verbose_name="Seller"
    )
    buyer = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name="", verbose_name="Buyer"
    )
    offer = models.ForeignKey(
        to=Offer, on_delete=models.PROTECT, related_name="", verbose_name="Offer"
    )
    deal_time = models.DateTimeField(auto_now=True, verbose_name="Time")

    def __str__(self):
        """String representation of the object."""
        return self.seller.username + " -> " + self.buyer.username

    class Meta:
        """Meta properties."""

        verbose_name = "Deal"
        verbose_name_plural = "Deals"
