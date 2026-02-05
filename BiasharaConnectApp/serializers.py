from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, BuyerProfile, SellerProfile
from django.db import transaction


class BuyerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)

    password = serializers.CharField(write_only=True)
    location = serializers.CharField(max_length=100)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered")
        return email

    def validate(self, data):
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            role="buyer",
        )

        BuyerProfile.objects.create(
            user=user,
            location=validated_data["location"],
        )

        return user


class SellerRegisterSerializer(serializers.Serializer):
    # Personal info
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)

    # Passwords
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # Business info
    business_name = serializers.CharField(max_length=255)
    business_type = serializers.ChoiceField(
        choices=SellerProfile.BUSINESS_TYPE_CHOICES
    )
    business_category = serializers.ChoiceField(
        choices=SellerProfile.CATEGORY_CHOICES
    )
    business_location = serializers.CharField(max_length=100)

    bio = serializers.CharField(
        required=False,
        allow_blank=True
    )

    profile_image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    # ---------------- VALIDATION ---------------- #

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered.")
        return email

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        validate_password(data["password"])
        return data

    # ---------------- CREATE ---------------- #

    @transaction.atomic
    def create(self, validated_data):
        profile_image = validated_data.pop("profile_image", None)
        bio = validated_data.pop("bio", "")
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            role="seller",
        )

        SellerProfile.objects.create(
            user=user,
            business_name=validated_data["business_name"],
            business_type=validated_data["business_type"],
            business_category=validated_data["business_category"],
            business_location=validated_data["business_location"],
            bio=bio,
            profile_image=profile_image,
        )

        return user
