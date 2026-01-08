from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Appointment, Case, ChatMessage

User = get_user_model()

# =====================================================
# AUTH
# =====================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")

    if not username or not password or not role:
        return Response({"error": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        role=role,
        status="approved" if role == "client" else "pending"
    )

    return Response({"message": "Signup successful"}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "status": user.status,
    })


# =====================================================
# CLIENT
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_advocates(request):
    if request.user.role != "client":
        return Response({"error": "Forbidden"}, status=403)

    advocates = User.objects.filter(role="advocate", status="approved")
    return Response(
        [{"id": a.id, "username": a.username} for a in advocates]
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    if request.user.role != "client":
        return Response({"error": "Only clients can book"}, status=403)

    advocate_id = request.data.get("advocate_id")
    date = request.data.get("date")
    time = request.data.get("time")

    if not advocate_id or not date or not time:
        return Response({"error": "All fields required"}, status=400)

    advocate = get_object_or_404(
        User, id=advocate_id, role="advocate", status="approved"
    )

    Appointment.objects.create(
        client=request.user,
        advocate=advocate,
        date=date,
        time=time,
        status="pending"
    )

    return Response({"message": "Appointment booked"}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_appointments(request):
    user = request.user

    if user.role == "client":
        apps = Appointment.objects.filter(client=user)
    elif user.role == "advocate":
        apps = Appointment.objects.filter(advocate=user)
    else:
        return Response([])

    return Response([
        {
            "id": a.id,
            "client": a.client.username,
            "advocate": a.advocate.username,
            "status": a.status,
            "date": a.date,
            "time": a.time,
        }
        for a in apps
    ])


# =====================================================
# ADMIN
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_advocates(request):
    if request.user.role != "admin":
        return Response({"error": "Forbidden"}, status=403)

    users = User.objects.filter(role="advocate", status="pending")
    return Response(
        [{"id": u.id, "username": u.username} for u in users]
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_advocate(request, user_id):
    if request.user.role != "admin":
        return Response({"error": "Forbidden"}, status=403)

    advocate = get_object_or_404(User, id=user_id, role="advocate")
    advocate.status = "approved"
    advocate.save()

    return Response({"message": "Advocate approved"})


# =====================================================
# ADVOCATE
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_appointment(request, appointment_id):
    if request.user.role != "advocate":
        return Response({"error": "Forbidden"}, status=403)

    appointment = get_object_or_404(
        Appointment, id=appointment_id, advocate=request.user
    )
    appointment.status = "approved"
    appointment.save()

    return Response({"message": "Appointment approved"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_case(request):
    if request.user.role != "advocate":
        return Response({"error": "Forbidden"}, status=403)

    client_id = request.data.get("client_id")
    title = request.data.get("title")
    description = request.data.get("description")

    if not client_id or not title or not description:
        return Response({"error": "All fields required"}, status=400)

    client = get_object_or_404(User, id=client_id, role="client")

    Case.objects.create(
        client=client,
        advocate=request.user,
        title=title,
        description=description
    )

    return Response({"message": "Case created"}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_cases(request):
    if request.user.role != "advocate":
        return Response({"error": "Forbidden"}, status=403)

    cases = Case.objects.filter(advocate=request.user)
    return Response([
        {
            "id": c.id,
            "client": c.client.username,
            "title": c.title,
            "description": c.description,
            "status": c.status
        }
        for c in cases
    ])


# =====================================================
# CHAT
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chat_history(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user not in [appointment.client, appointment.advocate]:
        return Response({"error": "Forbidden"}, status=403)

    if appointment.status != "approved":
        return Response({"error": "Chat not allowed"}, status=403)

    messages = ChatMessage.objects.filter(
        appointment=appointment
    ).order_by("timestamp")

    return Response([
        {
            "id": m.id,
            "sender": m.sender.username,
            "message": m.message,
            "file": m.file.url if m.file else None,
            "is_seen": m.is_seen,
            "time": m.timestamp,
        }
        for m in messages
    ])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user not in [appointment.client, appointment.advocate]:
        return Response({"error": "Forbidden"}, status=403)

    if appointment.status != "approved":
        return Response({"error": "Chat not allowed"}, status=403)

    msg = ChatMessage.objects.create(
        appointment=appointment,
        sender=request.user,
        message=request.data.get("message", "")
    )

    return Response({"id": msg.id})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_chat_file(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user not in [appointment.client, appointment.advocate]:
        return Response({"error": "Forbidden"}, status=403)

    if appointment.status != "approved":
        return Response({"error": "Chat not allowed"}, status=403)

    file = request.FILES.get("file")

    msg = ChatMessage.objects.create(
        appointment=appointment,
        sender=request.user,
        file=file
    )

    return Response({"file": msg.file.url})


# ============================
# 🔥 MISSING FUNCTIONS (FIX)
# ============================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_seen(request, appointment_id):
    ChatMessage.objects.filter(
        appointment_id=appointment_id,
        is_seen=False
    ).exclude(sender=request.user).update(is_seen=True)

    return Response({"status": "seen"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_count(request):
    count = ChatMessage.objects.filter(
        is_seen=False
    ).exclude(sender=request.user).count()

    return Response({"unread": count})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        advocate=request.user
    )
    appointment.delete()
    return Response({"message": "Deleted"})
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "role": getattr(user, "role", None),
    })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "username": request.user.username,
    })
