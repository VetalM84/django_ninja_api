"""Currency app URL Configuration."""

from django.urls import path

from currency.views import index

urlpatterns = [
    path("", index, name="index"),
]
