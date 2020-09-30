from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from model_utils import Choices
from .usermanagers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    STATUSES = Choices(
        (0, "pending", "pending"),  # email not verifies yet
        (1, "activated", "activated"),
        (-1, "blocked", "blocked"),
    )
    status = models.IntegerField(choices=STATUSES, default=STATUSES.pending)
    email = models.EmailField("email address", unique=True)
    full_name = models.CharField("full name", max_length=128, blank=True)
    is_staff = models.BooleanField("staff", default=False)
    is_superuser = models.BooleanField("super user", default=False)
    verification_code = models.CharField(
        max_length=6, null=True, blank=True, default=""
    )
    PROVIDER = Choices(
        ("SO", "social", "Social"),
        ("DE", "default", "System Generated"),
    )
    provider = models.CharField(
        max_length=2, choices=PROVIDER, default=PROVIDER.default
    )
    social_token = models.TextField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    # override the manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
