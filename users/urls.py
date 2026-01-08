from django.urls import path
from .views import signup, me, chat_messages

urlpatterns = [
    path("auth/signup/", signup),
    path("auth/me/", me),
    path("chat/<int:appointment_id>/", chat_messages),
]
