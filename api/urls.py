"""Main URLs endpoints"""

from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.routers import SimpleRouter


class OptionalSlashRouter(SimpleRouter):
    """OptionalSlashRouter"""

    def __init__(self):
        """Init"""
        super().__init__()
        self.trailing_slash = "/?"


urlpatterns = [
    path("", include("api.dawnet.urls")),
]
