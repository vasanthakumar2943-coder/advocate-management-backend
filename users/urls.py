from django.urls import path
from .views import (
    signup,
    login_view,
    me,
    pending_advocates,
    approve_advocate,
    delete_advocate,
    approved_advocates,
)

urlpatterns = [
    # =========================
    # AUTH
    # =========================
    path("signup/", signup),
    path("login/", login_view),
    path("me/", me),

    # =========================
    # ADMIN – ADVOCATE APPROVAL
    # =========================
    path("admin/pending-advocates/", pending_advocates),
    path("admin/approve-advocate/<int:id>/", approve_advocate),
    path("admin/delete-advocate/<int:id>/", delete_advocate),

    # =========================
    # CLIENT – APPROVED ADVOCATES
    # =========================
    path("approved-advocates/", approved_advocates),
]
