"""create models here"""
from typing import List

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from model_utils import Choices
import pgcrypto
from .usermanagers import UserManager
from ..models import LogsMixin


class UserAccountStatus(models.TextChoices):
    """enum choices for user status"""

    PENDING = "PENDING", "pending"
    ACTIVATED = "ACTIVATED", "activated"
    BLOCKED = "BLOCKED", "blocked"


class User(AbstractBaseUser, PermissionsMixin, LogsMixin):
    """User model, all information related to user accounts"""

    status = models.CharField(
        max_length=10,
        choices=UserAccountStatus.choices,
        default=UserAccountStatus.PENDING,
    )
    email = pgcrypto.EncryptedEmailField("Email Address", unique=True)
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
    """
    List (all fields) that will be prompted when creating a user via the createsuperuser command
    REQUIRED_FIELDS must contain all required fields on your user model,but should not contain
    USERNAME_FIELD or password as these fields will always be prompted.
    """
    REQUIRED_FIELDS: List = []


class EmailStatus(models.Model):
    """Model to keep Track of Email Sending Service"""

    user_email = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS = Choices(
        ("FA", "fail", "Fail"),
        ("SU", "success", "Success"),
        ("PE", "pending", "Pending"),
    )
    email_status = models.CharField(
        "Email Status", max_length=2, choices=STATUS, default=STATUS.pending)

    def __str__(self):
        return str(self.user_email)
