from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


# =========================
# User Model
# =========================
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, editable=False, db_index=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# =========================
# Buyer Profile
# =========================
class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Buyer: {self.user.email}"


# =========================
# Seller Profile
# =========================
class SellerProfile(models.Model):
    BUSINESS_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('cooperative', 'Cooperative'),
        ('partnership', 'Partnership'),
    )

    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Living'),
        ('food', 'Food'),
        ('automotive', 'Automotive'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES)
    business_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    business_location = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True, help_text="Short description about the seller or business")
    profile_image_url = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.user.email})"


# =========================
# Listing
# =========================
class Listing(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    )

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
        ('service', 'Service'),
    )

    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Living'),
        ('vehicles', 'Vehicles'),
        ('services', 'Services'),
        ('agriculture', 'Agriculture'),
    )

    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status', 'category'])]

    def activate(self):
        self.status = 'active'
        self.save(update_fields=['status'])

    def deactivate(self):
        self.status = 'inactive'
        self.save(update_fields=['status'])

    def soft_delete(self):
        self.status = 'deleted'
        self.save(update_fields=['status'])

    def __str__(self):
        return self.title


# =========================
# Listing Image
# =========================
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['listing'],
                condition=models.Q(is_primary=True),
                name='unique_primary_image_per_listing'
            )
        ]

    def __str__(self):
        return f"Image for {self.listing.title}"


# =========================
# Saved Listing
# =========================
class SavedListing(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'listing')

    def __str__(self):
        return f"{self.buyer.user.email} saved {self.listing.title}"
