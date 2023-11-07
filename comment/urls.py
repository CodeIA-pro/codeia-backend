"""
URL mapping for the user API.
"""
from django.urls import path, include
from comment import views

urlpatterns = [
    path('list/type/<int:type_id>/', views.ListCommentView.as_view(), name='list comment'),
    path('get/user/', views.GetCommentbyUserView.as_view(), name='get comment'),
    path('create/type/<int:type_id>/', views.CreateCommentView.as_view(), name='create comment'),
    path('update/<int:pk>/', views.UpdateCommentView.as_view(), name='update comment'),
    path('delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete comment'), 
]

