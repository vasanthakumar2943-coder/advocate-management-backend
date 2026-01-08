from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Appointment, Case, ChatMessage

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    user = User.objects.create_user(
        username=request.data["username"],
        password=request.data["password"],
        role=request.data["role"],
        status="approved"
    )
    return Response({"message": "Signup success"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "role": request.user.role,
    })


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def chat_messages(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user not in [appointment.client, appointment.advocate]:
        return Response({"error": "Forbidden"}, status=403)

    if request.method == "GET":
        msgs = ChatMessage.objects.filter(
            appointment=appointment
        ).order_by("created_at")

        return Response([
            {
                "sender": m.sender.username,
                "message": m.message,
                "created_at": m.created_at
            } for m in msgs
        ])

    if request.method == "POST":
        ChatMessage.objects.create(
            appointment=appointment,
            sender=request.user,
            message=request.data["message"]
        )
        return Response({"status": "sent"})
