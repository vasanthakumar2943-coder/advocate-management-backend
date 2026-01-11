from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from appointments.models import Appointment  # ✅ single correct import

User = get_user_model()

# =====================
# SIGNUP
# =====================
@api_view(["POST"])
def signup(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        if not username or not password or not role:
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_approved = True if role in ["admin", "client"] else False

        User.objects.create_user(
            username=username,
            password=password,
            role=role,
            is_approved=is_approved
        )

        return Response(
            {"message": "Signup successful"},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =====================
# LOGIN
# =====================
@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_403_FORBIDDEN
        )

    # ✅ FIX: BLOCK UNAPPROVED ADVOCATES
    if user.role == "advocate" and not user.is_approved:
        return Response(
            {"error": "Advocate account pending admin approval"},
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": user.role,
        "is_approved": user.is_approved,
    })


# =====================
# ME
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_approved": user.is_approved,
    })


# =====================
# ADMIN – PENDING ADVOCATES
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_advocates(request):
    if request.user.role != "admin":
        return Response({"error": "Forbidden"}, status=403)

    users = User.objects.filter(
        role="advocate",
        is_approved=False
    ).values("id", "username")

    return Response(list(users))


# =====================
# ADMIN – APPROVE ADVOCATE
# =====================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_advocate(request, id):
    if request.user.role != "admin":
        return Response({"error": "Forbidden"}, status=403)

    try:
        user = User.objects.get(id=id, role="advocate")
        user.is_approved = True
        user.save()
        return Response({"message": "Advocate approved"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# =====================
# ADMIN – DELETE ADVOCATE
# =====================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_advocate(request, id):
    if request.user.role != "admin":
        return Response({"error": "Forbidden"}, status=403)

    try:
        user = User.objects.get(id=id, role="advocate")
        user.delete()
        return Response({"message": "Advocate deleted"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# =====================
# CLIENT – APPROVED ADVOCATES LIST
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def approved_advocates(request):
    advocates = User.objects.filter(
        role="advocate",
        is_approved=True
    )

    data = []

    for adv in advocates:
        can_chat = False

        if request.user.role == "client":
            can_chat = Appointment.objects.filter(
                client=request.user,
                advocate=adv,
                status="approved"
            ).exists()

        data.append({
            "id": adv.id,
            "username": adv.username,
            "can_chat": can_chat
        })

    return Response(data)


# =====================
# CLIENT – CREATE APPOINTMENT
# =====================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    if request.user.role != "client":
        return Response({"error": "Only clients can book"}, status=403)

    advocate_id = request.data.get("advocate_id")  # ✅ FIX HERE

    if not advocate_id:
        return Response(
            {"error": "advocate_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    Appointment.objects.create(
        client=request.user,
        advocate_id=advocate_id,
        status="pending"
    )

    return Response({"message": "Booking successful"})
