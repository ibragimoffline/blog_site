from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
]
