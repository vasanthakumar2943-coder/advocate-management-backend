from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Users / Auth APIs
    path("api/", include("users.urls")),

    # Appointments APIs
    path("api/appointments/", include("appointments.urls")),
]
