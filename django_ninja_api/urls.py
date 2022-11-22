"""django_ninja_api URL Configuration."""

from django.contrib import admin
from django.urls import include, path

from currency.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", include("currency.urls")),
]
