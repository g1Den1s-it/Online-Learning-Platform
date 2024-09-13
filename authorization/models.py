from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

ROLE = (("Teacher", "Teacher"),
        ("Student", "Student"),
        ("Administrator", "Administrator"))


class User(AbstractUser):
    role = models.CharField(max_length=26, choices=ROLE, blank=False, default="Student")
