from byo_network_hub.models import GameEvent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger(__name__)


class GetGameEventView(APIView):
    permission_classes = [IsAuthenticated]  # R

    def get(self, request, user_id):

        logger.info(f"XYZ - HEADERS: {request.headers}")
        logger.info(f"XYZ - COOKIE: {request.COOKIES.get('sessionid')}")
        logger.info(f"XYZ - CSRF: {request.META.get('CSRF_COOKIE')}")
        logger.info(f"XYZ - USER: {request.user}")
        logger.info(f"XYZ - USER: {request.user.id}")

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
