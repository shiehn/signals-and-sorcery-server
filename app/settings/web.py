"""Settings for the WEB
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *
import os

APP_NAME = "web"

SITE_ID = 2


STATIC_URL = "/api/static/"


# SMTP EMAIL
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# # EMAIL_BACKEND = "app.email_logger.LoggingEmailBackend"
# EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 25))
# EMAIL_USE_LOCALTIME = False
#
# # Optional SMTP authentication information for EMAIL_HOST.
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
# EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"
#
# # If you don't use SSL, you can leave these as None or empty strings
# EMAIL_SSL_CERTFILE = os.getenv("EMAIL_SSL_CERTFILE", None)
# EMAIL_SSL_KEYFILE = os.getenv("EMAIL_SSL_KEYFILE", None)
# EMAIL_TIMEOUT = os.getenv("EMAIL_TIMEOUT", None)
