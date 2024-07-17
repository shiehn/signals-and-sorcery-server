from byo_network_hub.models import GameEvent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import logging

logger = logging.getLogger(__name__)


class GetGameEventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # logger.info(f"XYZ - USER: {request.user}")
        # logger.info(f"XYZ - USER_ID: {request.user.id}")

        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        event = GameEvent.objects.filter(user_id=user_id).order_by("created_at").first()
        if event:
            response = {
                "user_id": str(event.user_id),
                "event": event.event,
                "payload": event.payload,
                "created_at": event.created_at,
            }
            event.delete()
            return Response(response)
        return Response(
            {"error": "No event found for this user"}, status=status.HTTP_200_OK
        )


class AddGameEventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # R

    def post(self, request, user_id):
        try:
            data = request.data
            event_type = data.get(
                "event", "combat"
            )  # Default to 'combat' if no event type is provided
            event = GameEvent.objects.create(user_id=user_id, event=event_type)
            return Response(
                {"message": "Event added successfully", "event_id": event.id},
                status=status.HTTP_201_CREATED,
            )
        except (
            Exception
        ) as e:  # General exception catch if there's an error parsing JSON or saving the model
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
