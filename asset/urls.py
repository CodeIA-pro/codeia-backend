"""
URL mapping for the user API.
"""
from django.urls import path, include
from asset import views

urlpatterns = [
    path('list/', views.ListAssetView.as_view(), name='list asset'),
    path('create/project/<int:project_id>/', views.CreateAssetView.as_view(), name='create asset'),
    path('guide/<str:version>/project/<str:title>/repo/<str:user_repo>/', views.ListAssetByVersionView.as_view(), name='list asset by version'),
    path('create/<int:pk>/subsection/', views.CreatesSubSectionView.as_view(), name='create subasset'),
    path('update/<int:pk>/', views.UpdateAssetView.as_view(), name='update asset'),
    path('privacy/', views.PrivacyAssetStatusView.as_view(), name='update privacy asset'),
    path('delete/<int:pk>/', views.DeleteAssetView.as_view(), name='delete asset'),
]