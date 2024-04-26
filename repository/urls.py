"""
URL mapping for the user API.
"""
from django.urls import path, include
from repository import views

urlpatterns = [
    path('', views.ListRepositoryView.as_view(), name='list repository'),
    path('<str:name>/projects/', views.ListRepositoryToProjectView.as_view(), name='list repository projects'),
    path('name/<str:name>/', views.RetrieveRepositoryNameView.as_view(), name='retrieve project'),
    path('name/<str:name>/info/', views.RetrieveRepositoryNameInformationView.as_view(), name='retrieve project information'),
    path('create/', views.CreateRepositoryView.as_view(), name='create repository'),
    path('update/<int:pk>/', views.UpdateRepositoryView.as_view(), name='update repository'),
    path('add_project/repo/<int:pk>/project/<int:project_id>/', views.AddProjectToRepositoryView.as_view(), name='add project repository'),
    path('change_project/repo/<int:pk>/change_repo/<int:change_repo_id>/project/<int:project_id>/', views.ChangeRepositoryProjectView.as_view(), name='change project repository'),
]