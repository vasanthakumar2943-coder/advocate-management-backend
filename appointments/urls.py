from django.urls import path
from .views import (
    create_appointment,
    advocate_requests,
    approve_appointment
)

urlpatterns = [
    path("", create_appointment),                     # POST
    path("requests/", advocate_requests),             # GET ✅
    path("approve/<int:pk>/", approve_appointment),   # POST
]
