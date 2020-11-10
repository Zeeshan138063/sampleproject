"""urls for users module"""
from django.urls import path
from .views import LoginView, RefreshTokenView, UserSignUpAPIView, VerifyUserEmail

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("sign-up/", UserSignUpAPIView.as_view(), name="auth-login"),
    path("account-verification/<str:uid>/<str:token>/",
         VerifyUserEmail.as_view(),
         name="account-verification"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_jwt_token")
]
