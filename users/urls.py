from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # ==================================================
    # AUTH
    # ==================================================
    path("auth/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("auth/signup/", views.signup, name="signup"),
    path("auth/me/", views.me, name="me"),

    # ==================================================
    # CLIENT / ADVOCATE (COMMON)
    # ==================================================
    path("advocates/", views.list_advocates),
    path("appointments/book/", views.book_appointment),
    path("appointments/my/", views.my_appointments),

    # ==================================================
    # ADMIN
    # ==================================================
    path("admin/pending-advocates/", views.pending_advocates),
    path("admin/approve-advocate/<int:user_id>/", views.approve_advocate),

    # ==================================================
    # ADVOCATE
    # ==================================================
    path("advocate/approve-appointment/<int:appointment_id>/", views.approve_appointment),
    path("advocate/cases/create/", views.create_case),
    path("advocate/cases/my/", views.my_cases),

    # ==================================================
    # CHAT (REST)
    # ==================================================
    path("chat/<int:appointment_id>/history/", views.chat_history),
    path("chat/<int:appointment_id>/send/", views.send_message),
    path("chat/<int:appointment_id>/upload/", views.upload_chat_file),
    path("chat/<int:appointment_id>/mark-seen/", views.mark_seen),
    path("chat/unread-count/", views.unread_count),
]
