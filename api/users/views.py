"""views related user accounts creation and login"""

from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from api.users.exceptions import EmailAlreadyExistsError
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
            user = serializer.object.get("user")
            token = serializer.object.get("token")
            response_data = jwt_response_payload_handler(token, user, request)
            return self.send_success_response("Successfully logged in", response_data)

        # set the error message
        error_message = "Unable to log in with provided credentials."
        if "email" in serializer.errors:
            error_message = "Email is required."
        if "password" in serializer.errors:
            error_message = "Password is required."

        return self.send_bad_request_response(
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

            return self.send_success_response(
                "Token refreshed successfully.", response_data
            )

        return self.send_bad_request_response(description="Signature has expired.")


class UserSignUpAPIView(BaseAPIView):
    """ APIView class for user signup."""

    authentication_classes = ()  # type: ignore
    permission_classes = ()  # type: ignore

    def post(self, request):
        """Creates a new user in the system."""

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except EmailAlreadyExistsError:
                return self.send_bad_request_response(
                    description="User with this email already exists in the system."
                )

            return self.send_created_response(
                description="Congratulations! you are registered successfully.Confirm"
                            " your email to activate your account."
            )

        return self.send_bad_request_response(
            description="Failed to sign up.", errors=serializer.errors
        )
