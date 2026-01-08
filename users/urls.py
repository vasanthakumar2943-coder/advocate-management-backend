from django.urls import path
from .views import (
    signup,
    login_view,
    me,
    pending_advocates,
    approve_advocate,
)

urlpatterns = [
    path("auth/signup/", signup),
    path("auth/login/", login_view),
    path("me/", me),

    # 👇 ADMIN
    path("advocates/", pending_advocates),
    path("advocates/<int:id>/approve/", approve_advocate),
]
