"""
URL mapping for the user API.
"""
from django.urls import path, include
from forgotten import views

urlpatterns = [
    path('auth/', views.ForgottenPasswordView.as_view(), name='auth'),
    path('auth/password/reset/', views.ChangePasswordView.as_view(), name='auth-password-reset'),
]

