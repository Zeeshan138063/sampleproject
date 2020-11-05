"""Create your views here."""

from django.conf import settings
from rest_framework_jwt import authentication
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.status import is_server_error
from rest_framework.views import APIView


class BaseAPIView(APIView):
    """Base class for API views."""

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            "request": self.request,
            "view": self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def send_response(  # pylint: disable=no-self-use, bad-continuation, dangerous-default-value, too-many-arguments
        self,
        success=True,
        code="",
        status_code=status.HTTP_200_OK,
        payload=None,
        errors=None,
        description="",
    ):
        """
        Generates response.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload:dict  data generated for respective API call.
        :param errors: str description.
        :param description: str description.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                description = f"error message: {description}"
            else:
                description = "Internal server error."
        return Response(
            data={
                "success": success,
                "code": code,
                "payload": {} if payload is None else payload,
                "errors": {} if errors is None else errors,
                "description": description,
            },
            status=status_code,
        )

    def send_success_response(self, description, payload=None):
        """compose success response"""
        return self.send_response(
            status_code=status.HTTP_200_OK,
            payload={} if payload is None else payload,
            description=description,
        )

    def send_created_response(self, description, payload=None):
        """compose response for new object creation."""
        return self.send_response(
            status_code=status.HTTP_201_CREATED,
            payload={} if payload is None else payload,
            description=description,
        )

    def send_bad_request_response(self, description, errors=None):
        """compose response for bad request"""
        return self.send_response(
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            errors={} if errors is None else errors,
            description=description,
        )
