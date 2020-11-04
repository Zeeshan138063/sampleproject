"""urls for users module"""
from django.urls import path
from .views import LoginView, RefreshTokenView, UserSignUpAPIView

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("sign-up/", UserSignUpAPIView.as_view(), name="auth-login"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_jwt_token")
]
