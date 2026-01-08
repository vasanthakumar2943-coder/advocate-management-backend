from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["POST"])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", "client")

    if User.objects.filter(username=username).exists():
        return Response({"error": "User exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        role=role
    )
    return Response({"success": True})


@api_view(["GET"])
def me(request):
    user = request.user
    return Response({
        "username": user.username,
        "role": user.role,
        "status": getattr(user, "status", "approved"),
    })
