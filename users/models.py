from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class AdvocateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Appointment(models.Model):
    client = models.ForeignKey(
        User, related_name="client_appointments", on_delete=models.CASCADE
    )
    advocate = models.ForeignKey(
        User, related_name="advocate_appointments", on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id}"


class Case(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case {self.id}"


class ChatMessage(models.Model):
    appointment = models.ForeignKey(
        Appointment, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id}"
