"""
URL mapping for the user API.
"""
from django.urls import path, include
from plan import views

urlpatterns = [
    path('list/', views.ListPlanView.as_view(), name='list plan'),
    path('get/<int:pk>/', views.GetPlanView.as_view(), name='get plan'),
    path('create/', views.CreatePlanView.as_view(), name='create plan'),
    path('update/<int:pk>/', views.UpdatePlanView.as_view(), name='update plan'),
    path('delete/<int:pk>/', views.DeletePlanView.as_view(), name='delete plan'), 
]

