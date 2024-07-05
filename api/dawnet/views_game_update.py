# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from byo_network_hub.models import GameUpdateQueue
from .serializers import GameUpdateQueueSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class GetGameUpdateQueueByUserId(APIView):
    permission_classes = [IsAuthenticated]  # R

    def get(self, request, user_id):
        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        # Attempt to retrieve the GameUpdateQueue instance, return 404 if not found
        game_update = get_object_or_404(GameUpdateQueue, user_id=user_id)
        # Serialize the game update object
        serializer = GameUpdateQueueSerializer(game_update)
        return Response(serializer.data)
