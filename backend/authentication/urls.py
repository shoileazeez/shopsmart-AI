from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    LogoutView,
    PasswordResetRequestView,
    ResendPasswordResetCodeView,
    PasswordResetView,
)

urlpatterns = [
    path("user/register/", UserRegistrationView.as_view(), name="register"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password-reset/resend/", ResendPasswordResetCodeView.as_view(), name="resend_password_reset_code"),
    path("password-reset/confirm/", PasswordResetView.as_view(), name="password_reset_confirm"),
]