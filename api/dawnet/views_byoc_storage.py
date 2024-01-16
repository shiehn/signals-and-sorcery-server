import os
from datetime import timedelta

from django.http import JsonResponse
from google.cloud import storage
from google.cloud.storage import Blob
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from dawnet_client import SentryEventLogger, DNSystemType, DNTag, DNMsgStage
from mysite import settings

dn_tracer = SentryEventLogger(service_name=DNSystemType.DN_API_SERVER.value)

class SignedURLAPIView(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request):
        token = request.query_params.get('token')

        # Ensure the service account file exists
        service_account_file = settings.GCP_SERVICE_ACCOUNT_FILE
        if not os.path.exists(service_account_file):
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPLOAD_ASSET.value,
                DNTag.DNMsg.value: "Service account file not found.",
            })

            return JsonResponse({'error': 'Service account file not found.'}, status=500)

        # Retrieve the filename from query parameters
        original_filename = request.query_params.get('filename')
        if not original_filename:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPLOAD_ASSET.value,
                DNTag.DNMsg.value: "No filename specified.",
            })

            return JsonResponse({'error': 'No filename specified.'}, status=400)

        # Initialize the GCP Storage client
        try:
            storage_client = storage.Client.from_service_account_json(service_account_file)
            bucket = storage_client.get_bucket(settings.GCP_ASSET_BUCKET)
        except Exception as e:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPLOAD_ASSET.value,
                DNTag.DNMsg.value: str(e),
            })

            return JsonResponse({'error': str(e)}, status=500)

        # Create a blob with the original filename
        blob = Blob(original_filename, bucket)

        # Generate a signed URL for the upload
        try:
            signed_url = blob.generate_signed_url(version='v4', expiration=timedelta(minutes=15), method='PUT')
        except Exception as e:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPLOAD_ASSET.value,
                DNTag.DNMsg.value: str(e),
            })
            return JsonResponse({'error': str(e)}, status=500)

        dn_tracer.log_event(str(token), {
            DNTag.DNMsgStage.value: DNMsgStage.UPLOAD_ASSET.value,
            DNTag.DNMsg.value: "signed_url success",
        })

        return JsonResponse({'signed_url': signed_url})
