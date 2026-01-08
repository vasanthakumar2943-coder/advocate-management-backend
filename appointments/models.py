from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_apps")
    advocate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advocate_apps")
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved")],
        default="pending"
    )
