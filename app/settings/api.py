'''Settings for the API
'''

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *

APP_NAME = 'api'

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-language',
]

INSTALLED_APPS += [
	'corsheaders',
    'rest_framework',
]

MIDDLEWARE += [
	'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    )
}

SITE_ID = 1
