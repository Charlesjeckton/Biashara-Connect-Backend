from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def api_home(request):
    """
    Base API endpoint to verify the backend is reachable.
    """
    return Response({
        "name": "Biashara Connect API",
        "status": "running",
        "date": date.today()
    })
