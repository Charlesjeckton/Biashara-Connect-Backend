from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, BuyerProfile, SellerProfile, Listing, ListingImage, SavedListing


# =========================
# User Admin
# =========================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("email", "role", "is_staff", "is_verified", "is_active")
    list_filter = ("role", "is_staff", "is_verified", "is_active")
    search_fields = ("email",)
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# =========================
# Buyer Profile Admin
# =========================
@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location")
    search_fields = ("user__email", "location")


# =========================
# Seller Profile Admin
# =========================
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "profile_image_url",
        "business_name",
        "business_type",
        "business_category",
        "business_location",
        "is_verified",
    )
    list_filter = ("business_type", "is_verified")
    search_fields = ("user__email", "business_name")


# =========================
# Inline for Listing Images
# =========================
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ('image_url', 'is_primary')
    readonly_fields = ()
    # Enforce only one primary image per listing
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_primary')


# =========================
# Listing Admin
# =========================
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'condition', 'price', 'status', 'created_at')
    list_filter = ('status', 'category', 'condition', 'created_at', 'seller')
    search_fields = ('title', 'description', 'location', 'area')
    inlines = [ListingImageInline]
    actions = ['activate_listings', 'deactivate_listings', 'soft_delete_listings']

    # Admin actions
    def activate_listings(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"{updated} listing(s) activated.")
    activate_listings.short_description = "Activate selected listings"

    def deactivate_listings(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f"{updated} listing(s) deactivated.")
    deactivate_listings.short_description = "Deactivate selected listings"

    def soft_delete_listings(self, request, queryset):
        updated = queryset.update(status='deleted')
        self.message_user(request, f"{updated} listing(s) soft-deleted.")
    soft_delete_listings.short_description = "Soft delete selected listings"


# =========================
# Saved Listing Admin
# =========================
@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'listing', 'saved_at')
    search_fields = ('buyer__user__email', 'listing__title')