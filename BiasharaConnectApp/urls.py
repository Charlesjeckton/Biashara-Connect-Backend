from django.urls import path
from .views import (
    api_home,
    register_buyer,
    register_seller,
)

urlpatterns = [
    path("", api_home, name="api_home"),

    # Auth / Registration
    path("auth/register/buyer/", register_buyer, name="register_buyer"),
    path("auth/register/seller/", register_seller, name="register_seller"),
]
