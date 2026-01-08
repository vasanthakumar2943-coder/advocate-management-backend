from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_appointments(request):
    return Response([])

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_appointment(request, id):
    return Response({"message": "approved"})
