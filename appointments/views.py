from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Appointment


User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    advocate_id = request.data.get("advocate_id")

    if not advocate_id:
        return Response(
            {"error": "advocate_id required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    advocate = get_object_or_404(User, id=advocate_id)

    Appointment.objects.create(
        client=request.user,
        advocate=advocate,
        status="pending",
    )

    return Response(
        {"message": "Request sent"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def advocate_requests(request):
    appointments = Appointment.objects.filter(
        advocate=request.user,
        status="pending",
    )

    return Response(
        [
            {
                "id": appointment.id,
                "client": appointment.client.username,
            }
            for appointment in appointments
        ]
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_appointment(request, pk):
    appointment = get_object_or_404(
        Appointment,
        id=pk,
        advocate=request.user,
    )

    appointment.status = "approved"
    appointment.save()

    return Response({"message": "Approved"})
