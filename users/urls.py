from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    # AUTH
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/signup/", signup),
    path("auth/me/", me),

    # ADMIN
    path("admin/pending-advocates/", pending_advocates),
    path("admin/approve-advocate/<int:user_id>/", approve_advocate),

    # CLIENT
    path("client/advocates/", list_advocates),
    path("client/book-appointment/", book_appointment),
    path("client/my-appointments/", my_appointments),

    # ADVOCATE
    path("advocate/my-appointments/", my_appointments),
    path("advocate/approve-appointment/<int:appointment_id>/", approve_appointment),
    path("advocate/create-case/", create_case),
    path("advocate/my-cases/", my_cases),

    # CHAT
    path("chat/<int:appointment_id>/", chat_messages),
]
