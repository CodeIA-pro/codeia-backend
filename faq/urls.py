"""
URL mapping for the user API.
"""
from django.urls import path, include
from faq import views

urlpatterns = [
    path('list/', views.ListFAQView.as_view(), name='list faq'),
    path('get/<int:pk>/', views.GetFAQView.as_view(), name='get faq'),
    path('create/', views.CreateFAQView.as_view(), name='create faq'),
    path('update/<int:pk>/', views.UpdateFAQView.as_view(), name='update faq'),
    path('delete/<int:pk>/', views.DeleteFAQView.as_view(), name='delete faq'), 
]

