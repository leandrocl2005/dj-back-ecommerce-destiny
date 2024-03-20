from django.urls import path
from userauths import views as userauths_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(
        "user/token/",
        userauths_views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "user/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "user/register/",
        userauths_views.UserRegisterView.as_view(),
        name="user_register",
    ),
    path(
        "user/password-reset-email-verify/<str:email>/",
        userauths_views.PasswordResetEmailVerifyView.as_view(),
        name="password_reset_email_verify",
    ),
    path(
        "user/password-change",
        userauths_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
]
