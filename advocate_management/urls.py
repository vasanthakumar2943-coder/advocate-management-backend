from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # USERS APP (ALL APIs)
    path("api/", include("users.urls")),
]
