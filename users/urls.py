from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    # AUTH
    path("token/", TokenObtainPairView.as_view()),
    path("signup/", views.signup),
    path("me/", views.me),

    # CLIENT / ADVOCATE
    path("advocates/", views.list_advocates),
    path("appointments/book/", views.book_appointment),
    path("appointments/my/", views.my_appointments),

    # ADMIN
    path("pending-advocates/", views.pending_advocates),
    path("approve/<int:user_id>/", views.approve_advocate),

    # ADVOCATE
    path("approve-appointment/<int:appointment_id>/", views.approve_appointment),
    path("cases/create/", views.create_case),
    path("cases/my/", views.my_cases),

    # CHAT
    path("chat/<int:appointment_id>/", views.chat_history),
    path("chat/send/<int:appointment_id>/", views.send_message),
    path("chat/upload/<int:appointment_id>/", views.upload_chat_file),
    path("chat/seen/<int:appointment_id>/", views.mark_seen),
    path("chat/unread/", views.unread_count),
]
