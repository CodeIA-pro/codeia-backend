"""
URL mapping for the user API.
"""
from django.urls import path, include
from project import views

urlpatterns = [
    path('list/', views.ListProjectView.as_view(), name='list project'),
    path('get/<str:project>/owner/<str:owner>/', views.RetrieveProjectView.as_view(), name='get project'),
    path('info/<int:pk>/', views.RetrieveProjectInfoView.as_view(), name='info project'),
    path('create/', views.CreateProjectView.as_view(), name='create project'),
    path('update/<int:pk>/', views.UpdateProjectView.as_view(), name='update project'),
    path('delete/<int:pk>/', views.DeleteProjectView.as_view(), name='delete project'),
    path('connection/<str:code>/', views.GenerateConnectionGitHubView.as_view(), name='connection'),
    path('status/', views.ConnectionGitHubStatusView.as_view(), name='status'),
    path('<int:pk>/sha/', views.RetrieveSHAGitHubRepoView.as_view(), name='status'),
    path('get/github/user/', views.RetrieveGitHubUserInfo.as_view(), name='get github user'),
    path('get/github/repo/', views.RetrieveGitHubUserRepos.as_view(), name='get github repo'),
    path('get/github/branches/<str:repo>/owner/<str:owner>/', views.RetrieveGitHubRepoBranches.as_view(), name='get github branches'),
    path('get/github/languages/<str:repo>/owner/<str:owner>/', views.RetrieveGitHubRepoLanguages.as_view(), name='get github languages'),
    path('generate-connetion/<int:pk>/', views.GenerateConnectionView.as_view(), name='generate connection'), # deprecated
    path('guide-reference-completion/', views.GenerateAssetInformationView.as_view(), name='generate guia completion'),
    path('guide-reference/', views.GenerateAssetSubsectionView.as_view(), name='generate guia'),
    path('read-repo/<int:pk>/', views.RetrieveInformationGitHubRepoView.as_view(), name='read repo'),
    path('restore/,', views.DeleteGuiAssetView.as_view(), name='restore project'),
    path('runnig-guide/', views.GuideRunningView.as_view(), name='running guide'),
]