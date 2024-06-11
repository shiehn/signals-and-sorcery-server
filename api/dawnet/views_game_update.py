# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from byo_network_hub.models import GameUpdateQueue
from .serializers import GameUpdateQueueSerializer
from django.shortcuts import get_object_or_404


class GetGameUpdateQueueByUserId(APIView):
    def get(self, request, user_id):
        # Attempt to retrieve the GameUpdateQueue instance, return 404 if not found
        game_update = get_object_or_404(GameUpdateQueue, user_id=user_id)
        # Serialize the game update object
        serializer = GameUpdateQueueSerializer(game_update)
        return Response(serializer.data)
