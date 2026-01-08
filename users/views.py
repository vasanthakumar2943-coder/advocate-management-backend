from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def typing_status(request, appointment_id):
    key = f"typing_{appointment_id}_{request.user.id}"

    if request.method == "POST":
        cache.set(key, True, timeout=3)
        return Response({"typing": True})

    return Response({"typing": False})
