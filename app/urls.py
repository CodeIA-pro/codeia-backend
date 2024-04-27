"""
URL configuration for app project.
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [   
    path("admin/", admin.site.urls),
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="api-schema"
    ),  # genera el esquema de la API
    path(
        "prod",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("user/", include("user.urls"), name="user"),
    path("asset/", include("asset.urls"), name="asset"),
    path("project/", include("project.urls"), name="project"),
    path("faq/", include("faq.urls"), name="faq"),
    path("typecomment/", include("typecomment.urls"), name="typecomment"),
    path("comment/", include("comment.urls"), name="comment"),
    path("repository/", include("repository.urls"), name="repository"),
    path("forgotten/", include("forgotten.urls"), name="forgotten"),
]
