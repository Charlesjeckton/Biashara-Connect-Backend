from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Required by Django
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class BuyerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='buyer_profile'
    )
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Buyer: {self.user.email}"


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

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_profile'
    )

    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES)
    business_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)

    profile_image = models.ImageField(
        upload_to='seller_profiles/',
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Seller: {self.business_name}"
