from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# =====================
# SIGNUP
# =====================
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    data = request.data

    if User.objects.filter(username=data["username"]).exists():
        return Response({"error": "User exists"}, status=400)

    role = data.get("role", "client")

    user = User.objects.create_user(
        username=data["username"],
        password=data["password"],
        role=role,
        status="pending" if role == "advocate" else "approved",
    )

    return Response({"message": "Signup success"})


# =====================
# LOGIN
# =====================
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password"),
    )

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    if user.role == "advocate" and user.status != "approved":
        return Response(
            {"error": "Advocate account pending admin approval"},
            status=403
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "role": user.role,
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_advocates(request):
    if request.user.role != "admin":
        return Response(status=403)

    advocates = User.objects.filter(role="advocate", status="pending")
    data = [{"id": u.id, "username": u.username} for u in advocates]
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_advocate(request, id):
    if request.user.role != "admin":
        return Response(status=403)

    user = User.objects.get(id=id, role="advocate")
    user.status = "approved"
    user.save()
    return Response({"message": "Approved"})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_advocate(request, id):
    if request.user.role != "admin":
        return Response(status=403)

    User.objects.filter(id=id, role="advocate").delete()
    return Response({"message": "Deleted"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_advocate(request, id):
    if request.user.role != "admin":
        return Response({"error": "Unauthorized"}, status=403)

    user = User.objects.get(id=id, role="advocate")
    user.status = "approved"
    user.save()

    return Response({"message": "Advocate approved"})
