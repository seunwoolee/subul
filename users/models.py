from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    employeeNumber = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username + self.first_name