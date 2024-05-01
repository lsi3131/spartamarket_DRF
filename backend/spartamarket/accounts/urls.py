from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/<str:username>/", ProfileAPIView.as_view(), name="profile"),
    path("password/<str:username>/", PasswordAPIView.as_view(), name="password"),
    path("user_list/", UserListAPIView.as_view(), name="user_list"),
    path("delete/<str:username>/", DeleteUserAPIView.as_view(), name="delete"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("following/<str:username>/", FollowingAPIView.as_view(), name="following"),
]
