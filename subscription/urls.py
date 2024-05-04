"""
URL mapping for the user API.
"""
from django.urls import path, include
from subscription import views

urlpatterns = [
    path('list/', views.ListSubscriptionView.as_view(), name='list subscription'),
    path('get/<int:pk>/', views.GetSubscriptionView.as_view(), name='get subscription'),
    path('create/', views.GenerateSubscriptionView.as_view(), name='create subscription'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('get_user/', views.GetSubscriptionUserView.as_view(), name='get user subscription'),
    path('update/<int:pk>/', views.UpdateSubscriptionView.as_view(), name='update subscription'),
    path('delete/<int:pk>/', views.DeleteSubscriptionView.as_view(), name='delete subscription'), 
    path('cancel-subscription/', views.CancelSubscriptionView.as_view(), name='cancel subscription'),
]