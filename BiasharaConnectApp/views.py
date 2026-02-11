from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    BuyerRegisterSerializer,
    SellerRegisterSerializer,
    ListingSerializer,
    ListingCreateSerializer,
)
from .models import Listing, SavedListing


# =========================
# API Home
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def api_home(request):
    return Response({
        "name": "Biashara Connect API",
        "status": "running",
        "version": "1.0",
        "date": date.today().isoformat()
    })


# =========================
# Buyer Registration
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def register_buyer(request):
    serializer = BuyerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Buyer account created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# Seller Registration
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def register_seller(request):
    serializer = SellerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Seller account created successfully. Awaiting verification."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# User Login
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if not user:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }, status=status.HTTP_200_OK)


# =========================
# Listings
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def list_active_listings(request):
    """
    Get all active listings (buyers can view).
    """
    listings = Listing.objects.filter(status="active")
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_listing(request):
    """
    Sellers can create a listing with multiple Cloudinary image URLs.
    """
    if request.user.role != "seller":
        return Response({"error": "Only sellers can create listings"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ListingCreateSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Listing created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# Save / Unsave Listing
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_save_listing(request, listing_id):
    """
    Buyers can save or unsave a listing.
    """
    if request.user.role != "buyer":
        return Response({"error": "Only buyers can save listings"}, status=status.HTTP_403_FORBIDDEN)

    listing = Listing.objects.filter(id=listing_id, status="active").first()
    if not listing:
        return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

    saved, created = SavedListing.objects.get_or_create(buyer=request.user.buyer_profile, listing=listing)
    if not created:
        saved.delete()
        return Response({"message": "Listing unsaved"}, status=status.HTTP_200_OK)

    return Response({"message": "Listing saved"}, status=status.HTTP_200_OK)
