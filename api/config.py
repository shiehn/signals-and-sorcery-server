import os

# --------- PRODUCTION SETTINGS ----------------
API_BASE_URL = os.getenv("DN_WS_URL_BASE", "https://signalsandsorceryapi.com")
STORAGE_BUCKET_PATH = os.getenv(
    "DN_CLIENT_STORAGE_BUCKET", "https://storage.googleapis.com/byoc-file-transfer/"
)
