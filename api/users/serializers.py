"""Serializers fro sign up and login."""
from django.db import IntegrityError
from rest_framework import serializers

from utilities.utils import generate_code
from .models import User
from ..custom_exceptions import MyCustomError


class UserSerializer(serializers.ModelSerializer):
    """Serializers for user object"""

    class Meta:  # pylint: disable=missing-docstring
        model = User
        fields = ["email", "full_name", "last_login", "created_on", "modified_on"]


class SignUpSerializer(serializers.ModelSerializer):
    """Serialize for signup"""

    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField()

    class Meta:  # pylint: disable=missing-docstring
        model = User
        fields = ("full_name", "email", "password")

    def create(self, validated_data):  # pylint: disable=no-self-use
        """method to create the user object in db."""
        password = validated_data.pop("password")
        validated_data["verification_code"] = generate_code()
        validated_data["email"] = validated_data["email"].lower()

        record_exists = User.objects.filter(
            email__iexact=validated_data["email"]
        ).exists()
        # account with this email already exists. then quit further process.
        if record_exists:
            raise MyCustomError("User with this email already exists in the system.")
        try:
            validated_data["email"] = "zeeshan.iqbal@emumba.com"
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        except IntegrityError as error:
            raise error
