"""Currency app's DB models."""

from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    """Currency model."""

    code = models.CharField(
        max_length=3, unique=True, blank=False, null=False, verbose_name="Code"
    )
    country = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Country"
    )
    image = models.ImageField(verbose_name="Image")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        """Transform currency code to uppercase on save."""
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    class Meta:
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

    def __str__(self):
        return (
            self.currency_to_sell.code
            + " -> "
            + self.currency_to_buy.code
            + ": "
            + str(self.exchange_rate)
        )

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
