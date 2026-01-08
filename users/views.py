from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import AdvocateProfile, Appointment, Case, ChatMessage

User = get_user_model()

# =====================================================
# AUTH
# =====================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # ADMIN / CLIENT / ADVOCATE

    if not email or not password or not role:
        return Response({"error": "Missing fields"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(
        email=email,
        password=password,
        role=role,
    )

    if role == "ADVOCATE":
        AdvocateProfile.objects.create(user=user, approved=False)

    return Response({"message": "Signup successful"}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "email": user.email,
        "role": user.role,
    })


# =====================================================
# ADMIN
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_advocates(request):
    advocates = User.objects.filter(role="ADVOCATE")
    data = [{"id": a.id, "email": a.email} for a in advocates]
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_advocates(request):
    profiles = AdvocateProfile.objects.filter(approved=False)
    data = [{"id": p.user.id, "email": p.user.email} for p in profiles]
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_advocate(request, user_id):
    profile = get_object_or_404(AdvocateProfile, user_id=user_id)
    profile.approved = True
    profile.save()
    return Response({"message": "Advocate approved"})


# =====================================================
# CLIENT
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    advocate_id = request.data.get("advocate_id")
    advocate = get_object_or_404(User, id=advocate_id, role="ADVOCATE")

    appointment = Appointment.objects.create(
        client=request.user,
        advocate=advocate,
        approved=False,
    )
    return Response({"id": appointment.id})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_appointments(request):
    if request.user.role == "CLIENT":
        qs = Appointment.objects.filter(client=request.user)
    else:
        qs = Appointment.objects.filter(advocate=request.user)

    data = [{"id": a.id, "approved": a.approved} for a in qs]
    return Response(data)


# =====================================================
# ADVOCATE
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.approved = True
    appointment.save()
    return Response({"message": "Appointment approved"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_case(request):
    appointment_id = request.data.get("appointment_id")
    appointment = get_object_or_404(Appointment, id=appointment_id)

    case = Case.objects.create(
        appointment=appointment,
        description=request.data.get("description", "")
    )
    return Response({"id": case.id})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_cases(request):
    cases = Case.objects.filter(appointment__advocate=request.user)
    data = [{"id": c.id} for c in cases]
    return Response(data)


# =====================================================
# CHAT (REST ONLY)
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    msg = ChatMessage.objects.create(
        appointment=appointment,
        sender=request.user,
        message=request.data.get("message", "")
    )

    return Response({
        "id": msg.id,
        "message": msg.message,
        "is_me": True,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chat_history(request, appointment_id):
    messages = ChatMessage.objects.filter(
        appointment_id=appointment_id
    ).order_by("created_at")

    data = []
    for m in messages:
        data.append({
            "id": m.id,
            "message": m.message,
            "is_me": m.sender == request.user,
        })

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_chat_file(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    file = request.FILES.get("file")

    msg = ChatMessage.objects.create(
        appointment=appointment,
        sender=request.user,
        file=file,
    )

    return Response({"id": msg.id})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_seen(request, appointment_id):
    ChatMessage.objects.filter(
        appointment_id=appointment_id
    ).exclude(sender=request.user).update(seen=True)

    return Response({"message": "Seen"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_count(request):
    count = ChatMessage.objects.filter(
        seen=False
    ).exclude(sender=request.user).count()

    return Response({"unread": count})


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def typing_status(request, appointment_id):
    key = f"typing_{appointment_id}_{request.user.id}"

    if request.method == "POST":
        cache.set(key, True, timeout=3)
        return Response({"typing": True})

    return Response({"typing": False})
