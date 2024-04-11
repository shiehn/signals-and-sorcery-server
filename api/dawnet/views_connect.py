import json
import logging

from django.utils import timezone
from django.urls import resolve
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import ConnectionStatusSerializer
from byo_network_hub.models import ConnectionStatus


class Connect(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request, id=None):
        """
        This endpoint retrieves the connection status record(s) based on the provided connection token.
        """
        if id:
            # Retrieve the specific record by ID
            record = get_object_or_404(ConnectionStatus, id=id)

            # Serialize the record
            serializer = ConnectionStatusSerializer(record)

        else:
            # Retrieve all records from MyModel
            records = ConnectionStatus.objects.all()

            # Serialize the queryset
            serializer = ConnectionStatusSerializer(records, many=True)

        # Return serialized data as JSON
        return Response(serializer.data)

    def put(self, request, token, connection_status: int):
        """
        This endpoint updates the plugin or client connection status for a specified token.
        """
        # Determine the type based on the URL name
        url_name = resolve(request.path_info).url_name
        if url_name == "connection/compute":
            connection_type = "compute"
        else:
            connection_type = "plugin"

        logging.info(f"PUT_URL: {request.path_info}")

        # Check if a record with the provided token exists
        record, created = ConnectionStatus.objects.get_or_create(id=token)

        # Update the respective column and updated_at field
        current_time = timezone.now()
        if connection_type == "compute":
            record.compute = bool(connection_status)
            record.compute_updated_at = current_time  # Manually update the timestamp
        else:
            record.plugin = bool(connection_status)
            record.plugin_updated_at = current_time  # Manually update the timestamp

        # Save the updated/created record
        record.save()

        return Response(
            {
                "type": connection_type,
                "token": token,
                "status": connection_status,
                "record_created": created,
            }
        )


class UpdateLoadedStatus(APIView):
    def put(self, request, connection_token):
        """
        This endpoint updates the 'loaded' status for a specified connection token.
        """
        # Retrieve the record for the given token or return a 404 if not found
        record = get_object_or_404(ConnectionStatus, id=connection_token)

        # Parse the 'loaded' status from the request, expected as a boolean
        try:
            loaded_status = json.loads(request.body).get("loaded")
        except (json.JSONDecodeError, TypeError):
            return Response(
                {"error": "Invalid input format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate the loaded_status; it must be explicitly a boolean
        if loaded_status is None or not isinstance(loaded_status, bool):
            return Response(
                {"error": "'loaded' must be a boolean value and cannot be null"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the 'loaded' attribute and the updated_at field
        record.loaded = loaded_status

        # Save the updated record
        record.save()

        return Response(
            {"token": connection_token, "loaded_status": loaded_status},
            status=status.HTTP_200_OK,
        )
