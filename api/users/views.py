"""views related user accounts creation and login"""
from django.db import IntegrityError
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from api.custom_exceptions import MyCustomError
from api.users.serializers import UserSerializer, SignUpSerializer
from api.views import BaseAPIView


def jwt_response_payload_handler(token, user, request):
    """create response_data for jwt"""
    return {
        "token": token,
        "user": UserSerializer(user).data,
    }


class LoginView(ObtainJSONWebToken, BaseAPIView):
    """view to process the login."""

    authentication_classes = ()  # type: ignore
    permission_classes = ()  # type: ignore

    def post(self, request, *args, **kwargs):
        """login view."""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get("user") or request.user
            token = serializer.object.get("token")
            response_data = jwt_response_payload_handler(token, user, request)

            return self.send_response(
                success=True,
                payload=response_data,
                status_code=status.HTTP_200_OK,
                description="Successfully logged in",
            )
        # set the error message
        error_message = "Unable to log in with provided credentials."
        if "email" in serializer.errors:
            error_message = "Email is required."
        if "password" in serializer.errors:
            error_message = "Password is required."

        return self.send_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            description=error_message,
        )


class RefreshTokenView(RefreshJSONWebToken, BaseAPIView):
    """view to obtain a new token from old non-expired token."""

    def post(self, request, *args, **kwargs):
        """view to refresh token."""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get("user") or request.user
            token = serializer.object.get("token")
            response_data = jwt_response_payload_handler(token, user, request)

            return self.send_response(
                success=True,
                payload=response_data,
                status_code=status.HTTP_200_OK,
                description="Token refreshed successfully.",
            )
        error_message = "Signature has expired."

        return self.send_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            description=error_message,
        )


class UserSignUpAPIView(BaseAPIView):
    """ APIView class for user signup."""

    authentication_classes = ()  # type: ignore
    permission_classes = ()  # type: ignore

    def post(self, request):
        """
        Creates a new user in the system.
        """
        try:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return self.send_response(
                    success=True,
                    status_code=status.HTTP_201_CREATED,
                    description="Congratulations! you are registered successfully.Confirm"
                    " your email to activate your account.",
                )

            return self.send_response(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=serializer.errors,
            )
        except MyCustomError as e:
            return self.send_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                description=str(e),
            )
        except IntegrityError:
            message = "Problem with signup, You may retry after some time."
            return self.send_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                description=message,
            )
