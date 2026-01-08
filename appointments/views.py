from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    Appointment.objects.create(
        client=request.user,
        advocate_id=request.data["advocate"],
    )
    return Response({"message": "Request sent"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def advocate_requests(request):
    apps = Appointment.objects.filter(
        advocate=request.user, status="pending"
    )
    return Response([
        {"id": a.id, "client": a.client.username}
        for a in apps
    ])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_appointment(request, pk):
    app = Appointment.objects.get(id=pk, advocate=request.user)
    app.status = "approved"
    app.save()
    return Response({"message": "Approved"})
