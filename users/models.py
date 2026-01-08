from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # IMPORTANT: clash avoid panna related_name MUST
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="users_user_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username
