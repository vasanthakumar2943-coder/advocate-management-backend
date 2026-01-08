from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Appointment, Case, ChatMessage

User = get_user_model()


# =====================
# AUTH
# =====================
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    user = User.objects.create_user(
        username=request.data["username"],
        password=request.data["password"],
        role=request.data["role"],
        status="approved" if request.data["role"] == "client" else "pending",
    )
    return Response({"message": "Signup successful"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "role": request.user.role,
        "status": request.user.status,
    })


# =====================
# CLIENT
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_advocates(request):
    advocates = User.objects.filter(role="advocate", status="approved")
    return Response([{"id": a.id, "username": a.username} for a in advocates])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    advocate = get_object_or_404(
        User,
        id=request.data["advocate_id"],
        role="advocate",
        status="approved",
    )

    Appointment.objects.create(
        client=request.user,
        advocate=advocate,
        date=request.data["date"],
        time=request.data["time"],
    )
    return Response({"message": "Booked"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_appointments(request):
    if request.user.role == "client":
        qs = Appointment.objects.filter(client=request.user)
    else:
        qs = Appointment.objects.filter(advocate=request.user)

    return Response([
        {
            "id": a.id,
            "client": a.client.username,
            "advocate": a.advocate.username,
            "status": a.status,
        } for a in qs
    ])


# =====================
# ADMIN
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_advocates(request):
    users = User.objects.filter(role="advocate", status="pending")
    return Response([{"id": u.id, "username": u.username} for u in users])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_advocate(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = "approved"
    user.save()
    return Response({"message": "Approved"})


# =====================
# ADVOCATE
# =====================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_appointment(request, appointment_id):
    appt = get_object_or_404(
        Appointment,
        id=appointment_id,
        advocate=request.user
    )
    appt.status = "approved"
    appt.save()
    return Response({"message": "Approved"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_case(request):
    client = get_object_or_404(User, id=request.data["client_id"])
    Case.objects.create(
        client=client,
        advocate=request.user,
        title=request.data["title"],
        description=request.data["description"]
    )
    return Response({"message": "Case created"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_cases(request):
    cases = Case.objects.filter(advocate=request.user)
    return Response([
        {
            "id": c.id,
            "client": c.client.username,
            "title": c.title,
            "status": c.status,
        } for c in cases
    ])


# =====================
# CHAT (REST POLLING)
# =====================
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def chat_messages(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "GET":
        msgs = ChatMessage.objects.filter(
            appointment=appointment
        ).order_by("created_at")

        return Response([
            {
                "id": m.id,
                "sender": m.sender.username,
                "message": m.message,
                "created_at": m.created_at,
            } for m in msgs
        ])

    ChatMessage.objects.create(
        appointment=appointment,
        sender=request.user,
        message=request.data["message"]
    )
    return Response({"status": "sent"})
