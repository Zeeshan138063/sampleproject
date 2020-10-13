from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from api.users.constants import SIGN_UP_EMAIL_MESSAGE_BODY
from utilities.shared import ModuleCode, MessageTypeCode
from api.users.serializers import UserSerializer, SignUpSerializer
from api.views import BaseAPIView


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": UserSerializer(user, context={"request": request}).data,
    }


class LoginView(ObtainJSONWebToken, BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
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
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
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


class UserSignUpAPIView(BaseAPIView):
    """ APIView class for user signup."""

    authentication_classes = ()
    permission_classes = ()

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
                    code=f"201.{ModuleCode.USERS}.{MessageTypeCode.SUCCESS}",
                    status_code=status.HTTP_201_CREATED,
                    payload={},
                    description=SIGN_UP_EMAIL_MESSAGE_BODY,
                )

            else:
                return self.send_response(
                    code=f"422.{ModuleCode.USERS}.{MessageTypeCode.ERROR}",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors,
                )
        except Exception as e:
            return self.send_response(
                code=f"500.{ModuleCode.USERS}.{MessageTypeCode.EXCEPTION}",
                description=str(e),
            )
