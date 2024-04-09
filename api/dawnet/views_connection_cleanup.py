from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from byo_network_hub.models import ConnectionStatus


class ConnectionsCleanUp(APIView):
    authentication_classes = []  # Adjust as necessary
    permission_classes = []  # Adjust as necessary

    def get(self, request):
        # Calculate the threshold datetime: 24 hours ago from now
        threshold_time = timezone.now() - timedelta(hours=24)

        # Find records where neither plugin nor compute have been updated in the last 24 hours
        # This uses Q objects to create an OR condition between the two datetime fields
        outdated_connections = ConnectionStatus.objects.filter(
            Q(plugin_updated_at__lt=threshold_time)
            & Q(compute_updated_at__lt=threshold_time)
        )

        # Count the records to be deleted for the response
        count_deleted = outdated_connections.count()

        # Perform batch delete
        outdated_connections.delete()

        return Response(
            {"message": f"Deleted {count_deleted} outdated connection records."}
        )
