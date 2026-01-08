from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

# =====================
# SIGNUP (PUBLIC)
# =====================
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    data = request.data

    if User.objects.filter(username=data["username"]).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(
        username=data["username"],
        password=data["password"],
        role=data.get("role", "client"),
        status="pending" if data.get("role") == "advocate" else "approved",
    )

    return Response({"message": "Signup successful"}, status=201)


# =====================
# LOGIN (PUBLIC)
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

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })


# =====================
# ME (PROTECTED)
# =====================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "username": user.username,
        "role": user.role,
        "status": user.status,
    })
