"""views related user accounts creation and login"""
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken
from utilities.shared import ModuleCode, MessageTypeCode
from api.users.serializers import UserSerializer
from api.views import BaseAPIView


def jwt_response_payload_handler(token, user=None, request=None):
    """create response_data for jwt"""
    return {
        "token": token,
        "user": UserSerializer(user, context={"request": request}).data,
    }


class LoginView(ObtainJSONWebToken, BaseAPIView):
    """view to process the login."""

    authentication_classes = ()
    permission_classes = ()

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
                code=f"200.{ModuleCode.USERS}.{MessageTypeCode.ERROR}",
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
            payload={},
            code=f"400.{ModuleCode.USERS}.{MessageTypeCode.ERROR}",
            status_code=status.HTTP_400_BAD_REQUEST,
            description=error_message,
        )


class RefreshTokenView(RefreshJSONWebToken, BaseAPIView):
    """view to obtain a new token from old non-expired token."""

    authentication_classes = ()
    permission_classes = ()

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
                code=f"200.{ModuleCode.USERS}.{MessageTypeCode.ERROR}",
                status_code=status.HTTP_200_OK,
                description="Token refreshed successfully.",
            )
        error_message = "Signature has expired."

        return self.send_response(
            payload={},
            code=f"400.{ModuleCode.USERS}.{MessageTypeCode.ERROR}",
            status_code=status.HTTP_400_BAD_REQUEST,
            description=error_message,
        )
