from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utilities.utils import generate_code
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "last_login", "created_on", "modified_on"]


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.filter(status__gte=User.STATUSES.pending),
                message="User with this email already exists in the system..",
            )
        ]
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["verification_code"] = generate_code()
        # fixme: If user has already signed up but didn't verified email,
        #  returns to verification screen.
        validated_data["email"] = validated_data["email"].lower()
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()

        return user
