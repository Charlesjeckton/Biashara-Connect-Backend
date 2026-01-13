from datetime import date

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

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
