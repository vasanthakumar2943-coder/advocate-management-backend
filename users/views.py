from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

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

        # 🔥 Approval rule
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
        "status": user.status,
    })


# =====================
# ADMIN – PENDING ADVOCATES
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_advocates(request):
    users = User.objects.filter(
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
        return Response({"error": "Unauthorized"}, status=403)

    try:
        user = User.objects.get(id=id, role="advocate")
    except User.DoesNotExist:
        return Response({"error": "Advocate not found"}, status=404)

    user.status = "approved"
    user.save()

    return Response({"message": "Advocate approved"})


# =====================
# ADMIN – DELETE ADVOCATE
# =====================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_advocate(request, id):
    if request.user.role != "admin":
        return Response({"error": "Unauthorized"}, status=403)

    deleted, _ = User.objects.filter(id=id, role="advocate").delete()

    if deleted == 0:
        return Response({"error": "Advocate not found"}, status=404)

    return Response({"message": "Deleted"})


# =====================
# CLIENT – APPROVED ADVOCATES LIST ✅ (IMPORTANT)
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def approved_advocates(request):
    try:
        advocates = User.objects.filter(
            is_approved=True
        ).values("id", "username")

        return Response(list(advocates))
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=500
        )
# =====================
# ADVOCATE APPROVED NOTIFICATION 
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_approved": user.is_approved,
    })
