from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

class Member(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    membership_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
