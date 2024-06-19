from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import JSONParser
from byo_network_hub.models import GameMap
from .serializers import GameMapSerializer

from game_engine.api.environment import get_environment
from byo_network_hub.models import GameElementLookup


import logging

logger = logging.getLogger(__name__)


class GameEnvironmentView(APIView):
    """
    Retrieve or update a specific GameMap instance.
    """

    def get(self, request, environment_id):
        try:
            id = str(environment_id)

            # Attempt to get the user_id from GameElementLookup
            try:
                user_id = GameElementLookup.objects.get(element_id=id).user_id
            except GameElementLookup.DoesNotExist:
                logger.error(f"GameElementLookup with element_id {id} does not exist")
                raise Http404("GameElementLookup not found")

            # Retrieve the environment
            environment = get_environment(id, user_id)

            logger.info(f"XXX Environment: {environment}")

            return Response(environment, status=status.HTTP_200_OK)
        except GameMap.DoesNotExist:
            raise Http404("GameMap not found")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response(
                {"error": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
