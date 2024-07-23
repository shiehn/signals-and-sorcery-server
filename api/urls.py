"""Main URLs endpoints"""

from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter

# Since we're not using Swagger, we don't need re_path or the Swagger imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation for my project",
        terms_of_service="https://signalsandsorcery.com/",
        contact=openapi.Contact(email="stevehiehn@gmail.com"),
        license=openapi.License(name="GPL3 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class OptionalSlashRouter(SimpleRouter):
    """Router that makes the trailing slash optional."""

    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


urlpatterns = [
    path("", include("api.sas.urls")),
    # Swagger
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
