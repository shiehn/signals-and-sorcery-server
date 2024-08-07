"""Settings for the API
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *

APP_NAME = "api"

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-language",
]

INSTALLED_APPS += [
    "corsheaders",
    "game_models",
    "game_engine",
    "drf_yasg",
]

# MIDDLEWARE += [
#     "corsheaders.middleware.CorsMiddleware",
#     "api.middleware.RemoveWWWAuthenticateMiddleware",
# ]

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SITE_ID = 1

STATIC_URL = "/api/static/"
