from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('employee', 'Employee'),
        ('employer', 'Employer')
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username