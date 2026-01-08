from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import (
    signup,
    me,

    # Admin
    list_advocates,
    approve_advocate,
    pending_advocates,

    # Client / Advocate
    book_appointment,
    my_appointments,

    # Advocate
    approve_appointment,
    create_case,
    my_cases,

    # Chat
    send_message,
    chat_history,
    upload_chat_file,
    mark_seen,
    unread_count,
)

urlpatterns = [
    # ======================
    # DJANGO ADMIN
    # ======================
    path("admin/", admin.site.urls),

    # ======================
    # AUTH
    # ======================
    path("api/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/signup/", signup, name="signup"),
    path("api/", include("users.urls")),

    # ======================
    # ADMIN
    # ======================
    path("api/pending-advocates/", pending_advocates),
    path("api/approve/<int:user_id>/", approve_advocate),

    # ======================
    # CLIENT
    # ======================
    path("api/advocates/", list_advocates),
    path("api/book-appointment/", book_appointment),
    path("api/my-appointments/", my_appointments),

    # ======================
    # ADVOCATE
    # ======================
    path("api/appointments/my/", my_appointments),  # 🔥 SAME API FOR CLIENT & ADVOCATE
    path("api/approve-appointment/<int:appointment_id>/", approve_appointment),
    path("api/create-case/", create_case),
    path("api/my-cases/", my_cases),

    # ======================
    # CHAT (REST)
    # ======================
    path("api/chat/<int:appointment_id>/send/", send_message),
    path("api/chat-history/<int:appointment_id>/", chat_history),
    path("api/chat-upload/<int:appointment_id>/", upload_chat_file),
    path("api/mark-seen/<int:appointment_id>/", mark_seen),
    path("api/unread-count/", unread_count),
]
