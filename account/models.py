from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
import uuid


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4())
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
