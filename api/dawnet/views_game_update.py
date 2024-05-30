# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from byo_network_hub.models import GameUpdateQueue
from .serializers import GameUpdateQueueSerializer


class GetGameUpdateQueueByUserId(APIView):
    def get(self, request, user_id):
        # Attempt to retrieve or create a new GameUpdateQueue instance
        game_update, created = GameUpdateQueue.objects.get_or_create(
            user_id=user_id,
            defaults={
                "level": 1,
                "status": "queued",
            },  # Default values for new creation
        )
        # Serialize the game update object
        serializer = GameUpdateQueueSerializer(game_update)
        return Response(serializer.data)
