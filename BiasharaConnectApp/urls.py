from django.urls import path
from .views import (
    api_home,
    register_buyer,
    register_seller,
    login_user,
    list_active_listings,
    create_listing,
    toggle_save_listing,
)

app_name = "auth"

urlpatterns = [
    path("", api_home, name="api_home"),

    # Auth / Registration
    path("auth/register/buyer/", register_buyer, name="register_buyer"),
    path("auth/register/seller/", register_seller, name="register_seller"),

    # 🔑 LOGIN (Buyer + Seller)
    path("auth/login/", login_user, name="login"),

    # Listings
    path("listings/", list_active_listings, name="list_active_listings"),
    path("listings/create/", create_listing, name="create_listing"),

    # Saved listings (buyer)
    path("listings/<int:listing_id>/toggle-save/", toggle_save_listing, name="toggle_save_listing"),
]