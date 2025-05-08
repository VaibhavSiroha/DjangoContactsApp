from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

# -------------------------------------------
# Custom User Model
# -------------------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    number = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number.",
                code='invalid_number'
            )
        ]
    )
    is_verified = models.BooleanField(default=False)  # Set True after OTP verification

    def __str__(self):
        return self.username

# -------------------------------------------
# Contact Model
# -------------------------------------------
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number.",
                code='invalid_number'
            )
        ]
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'number'], name='unique_user_number')
        ]

    def __str__(self):
        return f"{self.name} - {self.number}"

# -------------------------------------------
# OTP Model
# -------------------------------------------
class Otp(models.Model):
    number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number.",
                code='invalid_number'
            )
        ]
    )
    otp = models.CharField(max_length=6)
    gtime = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.gtime + timedelta(minutes=5)

    def __str__(self):
        return f"{self.number} - {self.otp}"
