from datetime import date

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    BuyerRegisterSerializer,
    SellerRegisterSerializer
)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_home(request):
    """
    Base API endpoint to verify the backend is reachable.
    """
    return Response({
        "name": "Biashara Connect API",
        "status": "running",
        "version": "1.0",
        "date": date.today().isoformat()
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def register_buyer(request):
    serializer = BuyerRegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Buyer account created successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # authenticate uses USERNAME_FIELD (email in your case)
    user = authenticate(username=email, password=password)

    if user is None:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

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
