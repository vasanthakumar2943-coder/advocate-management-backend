from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# =====================================================
# USER MANAGER
# =====================================================

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="CLIENT"):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password, role="ADMIN")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# =====================================================
# USER MODEL
# =====================================================

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("CLIENT", "Client"),
        ("ADVOCATE", "Advocate"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CLIENT")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


# =====================================================
# ADVOCATE PROFILE
# =====================================================

class AdvocateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


# =====================================================
# APPOINTMENT
# =====================================================

class Appointment(models.Model):
    client = models.ForeignKey(
        User, related_name="client_appointments", on_delete=models.CASCADE
    )
    advocate = models.ForeignKey(
        User, related_name="advocate_appointments", on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# =====================================================
# CASE
# =====================================================

class Case(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# =====================================================
# CHAT MESSAGE
# =====================================================

class ChatMessage(models.Model):
    appointment = models.ForeignKey(
        Appointment, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
