from django.urls import path
from .views import admin_appointments, approve_appointment

urlpatterns = [
    path("admin/appointments/", admin_appointments),
    path("admin/appointments/<int:id>/approve/", approve_appointment),
]
