from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# =========================
# Custom User
# =========================
class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("advocate", "Advocate"),
        ("client", "Client"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return self.username


# =========================
# Appointment
# =========================
class Appointment(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_appointments"
    )
    advocate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="advocate_appointments"
    )
    date = models.DateField()
    time = models.TimeField()

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return f"{self.client} → {self.advocate}"


# =========================
# Case
# =========================
class Case(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cases"
    )
    advocate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="handled_cases"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=(("open", "Open"), ("closed", "Closed")),
        default="open"
    )


# =========================
# Chat Message (FINAL)
# =========================
class ChatMessage(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}"
