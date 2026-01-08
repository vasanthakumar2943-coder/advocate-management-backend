from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Appointment(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_appointments"
    )
    advocate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="advocate_appointments",
        null=True,
        blank=True
    )
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        default="pending"   # pending / approved
    )

    def __str__(self):
        return f"{self.client} → {self.advocate}"
