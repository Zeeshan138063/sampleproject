from django.urls import path
from rest_framework_jwt.views import verify_jwt_token
from .views import LoginView, RefreshTokenView, UserSignUpAPIView

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("sign-up/", UserSignUpAPIView.as_view(), name="auth-login"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_jwt_token"),
    path("verify-token/", verify_jwt_token),
]
