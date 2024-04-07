from django.db.models import F, Q, ExpressionWrapper, fields
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from byo_network_hub.models import ConnectionStatus


class ConnectionsTimeout(APIView):
    authentication_classes = []  # Disables authentication, for example purposes
    permission_classes = []  # Disables permission checks, for example purposes

    def get(self, request):
        # Define the threshold in seconds
        threshold_seconds = 10
        threshold_time = timezone.now() - timedelta(seconds=threshold_seconds)

        # Query to find all records that need updating
        # We use Q objects for OR conditions and F expressions to compare field values
        query = Q(plugin=True, plugin_updated_at__lt=threshold_time) | Q(
            compute=True, compute_updated_at__lt=threshold_time
        )

        # Select the relevant records
        outdated_connections = ConnectionStatus.objects.filter(query)

        # Iterate and update in memory (not in the database yet)
        for connection in outdated_connections:
            if connection.plugin and connection.plugin_updated_at < threshold_time:
                connection.plugin = False
            if connection.compute and connection.compute_updated_at < threshold_time:
                connection.compute = False

        # Batch update
        ConnectionStatus.objects.bulk_update(
            outdated_connections, ["plugin", "compute"]
        )

        return Response({"message": "Connection statuses updated"})
