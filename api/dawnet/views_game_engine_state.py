import uuid

from django.db import transaction
from rest_framework import generics
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from game_engine.api.map_inspector import MapInspector
from byo_network_hub.models import (
    GameState,
    GameMap,
    GameElementLookup,
    GameUpdateQueue,
)
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator
from game_engine.api.level_up import level_up
from .serializers import GameStateSerializer
import logging
from rest_framework.views import APIView
from game_engine.api.environment import get_environment
from byo_network_hub.models import GameElementLookup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError

logger = logging.getLogger(__name__)

GENERATE_ASSETS_ON_GAME_STATE_CREATE = False


def add_uuids_to_lookup(user_id, uuids):
    with transaction.atomic():  # Start a new transaction
        for uuid in uuids:
            GameElementLookup.objects.create(element_id=uuid, user_id=user_id)


class GameStateCreateView(generics.CreateAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer

    def perform_create(self, serializer):
        open_ai_key = self.kwargs.get("open_ai_key")
        logger = logging.getLogger(__name__)

        if open_ai_key:
            logger.info(f"OpenAI Key: {open_ai_key}")
        else:
            logger.error("No OpenAI Key provided")
            raise ValueError("No OpenAI Key provided")

        user_id = serializer.validated_data["user_id"]

        game_update, _ = GameUpdateQueue.objects.get_or_create(
            user_id=user_id, defaults={"level": 1, "status": "started"}
        )

        game_update.status = "started"
        game_update.save()

        try:
            # map_generator = MapGenerator()
            # unprocessed_map = map_generator.generate(
            #     num_rooms=int(game_update.level) + 2, percent_connected=0.25
            # ).get_json()
            #
            # processed_map = MapProcessor(unprocessed_map)
            # processed_map = processed_map.add_entrance_exit()
            # processed_map = processed_map.add_items()
            # processed_map = processed_map.add_encounters()
            #
            # map = processed_map.get_map()
            #
            # game_map = GameMap.objects.create(
            #     level=game_update.level,
            #     description=serializer.validated_data["aesthetic"],
            #     map_graph=map,
            # )
            #
            # map_inspector = MapInspector(map)
            # uuids = map_inspector.extract_uuids()
            # add_uuids_to_lookup(user_id, uuids)
            #
            # entrance_env_id = map_inspector.get_env_id_of_entrance()
            # entrance_env_img = map_inspector.get_env_by_id(entrance_env_id)[
            #     "game_info"
            # ]["environment"]["aesthetic"]["image"]
            #
            # logger.info(f"Calculated environment_id: {entrance_env_id}")
            # logger.info(f"Calculated environment_img: {entrance_env_img}")
            #
            # serializer.validated_data["map_id"] = game_map.id
            # serializer.validated_data["environment_id"] = entrance_env_id
            # serializer.validated_data["environment_img"] = entrance_env_img

            logger.info(f"Validated data before save: {serializer.validated_data}")

            serializer.save()

            game_update.status = "queued"
            game_update.save()

        except Exception as e:
            logger.error(f"Error during GameState creation: {str(e)}")
            game_update.status = "error"
            game_update.save()
            raise e


class GameStateDetailView(generics.RetrieveAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "user_id"


class GameStateDeleteView(generics.DestroyAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "user_id"


class GameStateUpdateView(generics.UpdateAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "id"


class LevelUpView(APIView):
    """
    Level UP the users game
    """

    def get(self, request, environment_id):
        try:
            response = level_up(environment_id)
            return Response(response, status=status.HTTP_200_OK)
        except GameMap.DoesNotExist:
            raise HttpResponseServerError
