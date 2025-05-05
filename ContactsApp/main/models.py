from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)  # Ensure email is unique
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

    def __str__(self):
        return self.username

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

    def __str__(self):
        return f"{self.name} - {self.number}"
