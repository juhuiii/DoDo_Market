from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
