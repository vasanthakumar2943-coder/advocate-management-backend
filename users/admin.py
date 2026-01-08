from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AdvocateProfile, Appointment, Case, ChatMessage


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Role", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(AdvocateProfile)
admin.site.register(Appointment)
admin.site.register(Case)
admin.site.register(ChatMessage)
