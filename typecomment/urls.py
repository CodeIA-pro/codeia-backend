"""
URL mapping for the user API.
"""
from django.urls import path, include
from typecomment import views

urlpatterns = [
    path('list/', views.ListTypeCommentView.as_view(), name='list typecomment'),
    path('get/<int:pk>/', views.GetTypeCommentView.as_view(), name='get typecomment'),
    path('create/', views.CreateTypeCommentView.as_view(), name='create typecomment'),
    path('update/<int:pk>/', views.UpdateTypeCommentView.as_view(), name='update typecomment'),
    path('delete/<int:pk>/', views.DeleteTypeCommentView.as_view(), name='delete typecomment'), 
]

