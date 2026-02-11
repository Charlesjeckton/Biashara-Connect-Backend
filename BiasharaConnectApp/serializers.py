from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from .models import User, BuyerProfile, SellerProfile, ListingImage, Listing, SavedListing


# =========================
# Buyer Registration
# =========================
class BuyerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    location = serializers.CharField(max_length=100)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered.")
        return email

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            role="buyer",
        )
        BuyerProfile.objects.create(user=user, location=validated_data["location"])
        return user


# =========================
# Seller Registration
# =========================
class SellerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    business_name = serializers.CharField(max_length=255)
    business_type = serializers.ChoiceField(choices=SellerProfile.BUSINESS_TYPE_CHOICES)
    business_category = serializers.ChoiceField(choices=SellerProfile.CATEGORY_CHOICES)
    business_location = serializers.CharField(max_length=100)
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.URLField(required=False, allow_null=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered.")
        return email

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        validate_password(data["password"])
        return data

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


# =========================
# Listing Image Serializer
# =========================
class ListingImageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = ListingImage
        fields = ("id", "image", "is_primary")


# =========================
# Listing Serializer
# =========================
class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    seller_name = serializers.SerializerMethodField()
    seller_verified = serializers.BooleanField(source="seller.is_verified", read_only=True)
    seller_image = serializers.URLField(source="seller.profile_image", read_only=True)

    class Meta:
        model = Listing
        fields = (
            "id", "seller", "seller_name", "seller_verified", "seller_image",
            "title", "description", "price", "category", "condition",
            "location", "area", "status", "created_at", "updated_at", "images"
        )
        read_only_fields = ("seller", "status", "created_at", "updated_at")

    def get_seller_name(self, obj):
        if obj.seller and obj.seller.user:
            return f"{obj.seller.user.first_name} {obj.seller.user.last_name}"
        return "Seller"


# =========================
# Saved Listing Serializer
# =========================
class SavedListingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = SavedListing
        fields = ("id", "buyer", "listing", "saved_at")
        read_only_fields = ("buyer", "saved_at")


# =========================
# Listing Create Serializer
# =========================
class ListingCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "description",
            "price",
            "category",
            "condition",
            "location",
            "area",
            "images",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        images_data = validated_data.pop("images", [])

        # Get seller safely
        if not hasattr(request.user, "seller_profile"):
            raise serializers.ValidationError("User does not have a seller profile.")

        seller = request.user.seller_profile

        # Create listing
        listing = Listing.objects.create(
            seller=seller,
            **validated_data
        )

        # Create images
        for index, image in enumerate(images_data):
            ListingImage.objects.create(
                listing=listing,
                image=image,
                is_primary=(index == 0)  # first image = primary
            )

        return listing

    def to_representation(self, instance):
        """Return images in response"""
        representation = super().to_representation(instance)
        representation["images"] = ListingImageSerializer(
            instance.images.all(), many=True
        ).data
        return representation
