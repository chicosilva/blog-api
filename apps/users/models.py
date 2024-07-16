import datetime
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from apps.users.choices import UserType

from .managers import CustomerManager, CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    user_type = models.CharField(max_length=30, choices=UserType.choices)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    canceled_at = models.DateTimeField(editable=False, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    customers = CustomerManager()

    def __str__(self) -> str:
        return f"{self.first_name}"

    @property
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def set_canceled(self):
        self.canceled_at = datetime.datetime.now()
        return self

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
