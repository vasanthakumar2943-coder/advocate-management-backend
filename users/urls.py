from django.urls import path
from .views import (
    signup,
    login_view,
    me,
    pending_advocates,
    approve_advocate,
    delete_advocate,
    approved_advocates,   # ✅ ADD THIS
)

urlpatterns = [
    # auth
    path("signup/", signup),
    path("login/", login_view),
    path("me/", me),

    # admin – advocate approval
    path("admin/pending-advocates/", pending_advocates),
    path("admin/approve-advocate/<int:id>/", approve_advocate),
    path("admin/delete-advocate/<int:id>/", delete_advocate),

    # client – approved advocates list ✅
    path("approved-advocates/", approved_advocates),
]
