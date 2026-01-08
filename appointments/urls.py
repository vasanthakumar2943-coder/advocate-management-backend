from django.urls import path
from .views import create_appointment, advocate_requests, approve_appointment

urlpatterns = [
    path("appointments/", create_appointment),
    path("appointments/requests/", advocate_requests),
    path("appointments/approve/<int:pk>/", approve_appointment),
]
