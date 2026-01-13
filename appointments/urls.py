from django.urls import path
from .views import delete_appointment
from .views import (
    create_appointment,
    advocate_requests,
    approve_appointment,
    approved_clients,
    appointments_root,
    delete_appointment,
)

urlpatterns = [
    # ✅ ROOT (fixes /api/appointments 404)
    path("", appointments_root),                 # GET

    # ✅ CREATE appointment (client → advocate)
    path("create/", create_appointment),         # POST

    # 🔴 Advocate pending requests
    path("requests/", advocate_requests),        # GET

    # 🟢 Advocate approved clients
    path("approved/", approved_clients),         # GET

    # ✅ Approve appointment
    path("approve/<int:pk>/", approve_appointment),  # POST

    path("delete/<int:pk>/", delete_appointment),     # DELETE ✅
]
