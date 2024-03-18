from django.urls import path
from userauths import views as userauths_views

urlpatterns = [
    path(
        "user/token/",
        userauths_views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "user/register/",
        userauths_views.UserRegisterView.as_view(),
        name="user_register",
    ),
]
