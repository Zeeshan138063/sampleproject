"""create models here"""
from typing import List

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from model_utils import Choices
from .usermanagers import UserManager
from ..models import LogsMixin


class User(AbstractBaseUser, PermissionsMixin, LogsMixin):
    """User model, all information related to user accounts"""

    STATUSES = Choices(
        (0, "pending", "pending"),  # email not verifies yet
        (1, "activated", "activated"),
        (-1, "blocked", "blocked"),
    )
    status = models.IntegerField(choices=STATUSES, default=STATUSES.pending)
    email = models.EmailField("Email Address", unique=True)
    full_name = models.CharField("Full Name", max_length=128, blank=True)
    is_staff = models.BooleanField("Is Staff", default=False)
    is_superuser = models.BooleanField("Is Super User", default=False)
    verification_code = models.CharField(
        "Verification Code", max_length=6, null=True, blank=True, default=None
    )
    PROVIDER = Choices(
        ("SO", "social", "Social"),
        ("DE", "default", "System Generated"),
    )
    provider = models.CharField(
        max_length=2, choices=PROVIDER, default=PROVIDER.default
    )

    # override the manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["email"]
