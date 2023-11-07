"""
URL mapping for the user API.
"""
from django.urls import path, include
from project import views

urlpatterns = [
    path('list/', views.ListProjectView.as_view(), name='list project'),
    path('get/<int:pk>/', views.RetrieveProjectView.as_view(), name='get project'),
    path('create/', views.CreateProjectView.as_view(), name='create project'),
    path('update/<int:pk>/', views.UpdateProjectView.as_view(), name='update project'),
    path('delete/<int:pk>/', views.DeleteProjectView.as_view(), name='delete project'),
]