from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)  # Email must be unique globally
    number = models.CharField(
        max_length=10,
        unique=True,  # Each user must have a unique personal number
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number.",
                code='invalid_number'
            )
        ]
    )

    def __str__(self):
        return self.username


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)  # ❌ Removed unique=True to allow same email for multiple users
    number = models.CharField(
        max_length=10,
        validators=[  # ❌ Removed unique=True so that multiple users can save same number
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number.",
                code='invalid_number'
            )
        ]
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        # ✅ Ensures a user cannot save the same number more than once
        constraints = [
            models.UniqueConstraint(fields=['user', 'number'], name='unique_user_number')
        ]

    def __str__(self):
        return f"{self.name} - {self.number}"