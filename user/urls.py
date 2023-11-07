"""
URL mapping for the user API.
"""
from django.urls import path, include
from user import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("user/", views.ManageUserView.as_view(), name="user"),
    path("admin/list/", views.ListUserViewAdmin.as_view(), name="user-admin"),
    path("admin/<int:pk>/", views.UpdateUserViewAdmin.as_view(), name="user-admin-update"),
]
