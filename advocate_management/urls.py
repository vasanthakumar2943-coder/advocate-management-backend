from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    # Auth
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

    # Chat (REST)
    send_message,
    chat_history,
    upload_chat_file,
    mark_seen,
    unread_count,
)

urlpatterns = [
    # ==================================================
    # DJANGO ADMIN
    # ==================================================
    path("admin/", admin.site.urls),

    # ==================================================
    # AUTH / JWT
    # ==================================================
    path("api/auth/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("api/auth/signup/", signup, name="signup"),
    path("api/auth/me/", me, name="me"),

    # ==================================================
    # ADMIN APIs
    # ==================================================
    path("api/admin/advocates/", list_advocates),
    path("api/admin/pending-advocates/", pending_advocates),
    path("api/admin/approve-advocate/<int:user_id>/", approve_advocate),

    # ==================================================
    # CLIENT APIs
    # ==================================================
    path("api/client/book-appointment/", book_appointment),
    path("api/client/my-appointments/", my_appointments),

    # ==================================================
    # ADVOCATE APIs
    # ==================================================
    path("api/advocate/my-appointments/", my_appointments),
    path("api/advocate/approve-appointment/<int:appointment_id>/", approve_appointment),
    path("api/advocate/create-case/", create_case),
    path("api/advocate/my-cases/", my_cases),

    # ==================================================
    # CHAT APIs (REST)
    # ==================================================
    path("api/chat/<int:appointment_id>/send/", send_message),
    path("api/chat/<int:appointment_id>/history/", chat_history),
    path("api/chat/<int:appointment_id>/upload/", upload_chat_file),
    path("api/chat/<int:appointment_id>/mark-seen/", mark_seen),
    path("api/chat/unread-count/", unread_count),

    # ==================================================
    # APP URLS (OPTIONAL – FUTURE SCALE)
    # ==================================================
    path("api/", include("users.urls")),
]
