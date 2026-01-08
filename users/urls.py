from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import *

urlpatterns = [

    # AUTH
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/signup/", signup),
    path("auth/me/", me),

    # ADMIN
    path("admin/advocates/", list_advocates),
    path("admin/pending-advocates/", pending_advocates),
    path("admin/approve-advocate/<int:user_id>/", approve_advocate),

    # CLIENT
    path("client/book-appointment/", book_appointment),
    path("client/my-appointments/", my_appointments),

    # ADVOCATE
    path("advocate/my-appointments/", my_appointments),
    path("advocate/approve-appointment/<int:appointment_id>/", approve_appointment),
    path("advocate/create-case/", create_case),
    path("advocate/my-cases/", my_cases),

    # CHAT (REST ONLY)
    path("chat/<int:appointment_id>/send/", send_message),
    path("chat/<int:appointment_id>/history/", chat_history),
    path("chat/<int:appointment_id>/upload/", upload_chat_file),
    path("chat/<int:appointment_id>/mark-seen/", mark_seen),
    path("chat/<int:appointment_id>/typing/", typing_status),
    path("chat/unread-count/", unread_count),
]
