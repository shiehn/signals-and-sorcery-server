import os
import requests

from google.cloud import storage
from google.cloud.storage import Blob
from datetime import timedelta

# API_BASE_URL = os.environ.get("API_BASE_URL", "https://localhost:8000")
# API_BASE_URL = "https://localhost:8081"
STORAGE_BUCKET_PATH = "https://storage.googleapis.com/byoc-file-transfer/"


class FileUploader:
    def get_signed_url(self, filename, token) -> str:
        # Ensure the service account file exists
        service_account_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")

        # Initialize the GCP Storage client
        storage_client = storage.Client.from_service_account_json(service_account_file)
        bucket_name = os.environ.get("GCP_ASSET_BUCKET")
        bucket = storage_client.bucket(bucket_name)
        blob = Blob(filename, bucket)

        # Generate a signed URL for the upload
        signed_url = blob.generate_signed_url(
            version="v4", expiration=timedelta(minutes=15), method="PUT"
        )

        return signed_url

    def upload_file_to_gcp(self, file_path, signed_url, file_type) -> bool:
        with open(file_path, "rb") as file:
            response = requests.put(
                signed_url, data=file, headers={"Content-Type": file_type}
            )
            return response.status_code == 200

    def upload(self, file_path, file_type) -> str:
        file_name = os.path.basename(file_path)
        storage_bucket_path = STORAGE_BUCKET_PATH.rstrip("/")
        file_url = f"{storage_bucket_path}/{file_name}"
        signed_url = self.get_signed_url(file_name, "myToken")
        result = self.upload_file_to_gcp(file_path, signed_url, file_type)

        if result:
            return file_url
        else:
            raise Exception("Failed to upload file to GCP")
