"""Serializers fro sign up and login."""
from django.db import IntegrityError
from rest_framework import serializers

from utilities.utils import generate_code
from .exceptions import EmailAlreadyExistsError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializers for user object"""

    class Meta:  # pylint: disable=missing-docstring
        model = User
        fields = ["email", "full_name", "last_login", "created_on", "modified_on"]


class SignUpSerializer(serializers.ModelSerializer):
    """Serialize for signup"""

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)  # call the super()
        for field in self.fields:  # iterate over the serializer fields
            self.fields[field].error_messages[
                'required'] = f'{field.title()} field is required'  # set the custom error message

    password = serializers.CharField(write_only=True, min_length=6, required=True)
    email = serializers.EmailField()

    class Meta:  # pylint: disable=missing-docstring
        model = User
        fields = ("full_name", "email", "password")

    def create(self, validated_data):  # pylint: disable=no-self-use
        """create the user object in db."""
        password = validated_data.pop("password")
        validated_data["verification_code"] = generate_code()
        validated_data["email"] = validated_data["email"].lower()

        try:
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        except IntegrityError as error:
            if hasattr(error, 'args') and "duplicate key value violates" in error.args[0]:
                raise EmailAlreadyExistsError
