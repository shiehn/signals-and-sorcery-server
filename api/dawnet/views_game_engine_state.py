import uuid

from django.db import transaction
from rest_framework import generics
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from game_engine.api.map_inspector import MapInspector
from game_engine.api.item_generator import ItemGenerator
from byo_network_hub.models import (
    GameState,
    GameInventory,
    GameMap,
    GameElementLookup,
    GameUpdateQueue,
    GameMapState,
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


def delete_user_related_objects(user_id):
    # Delete GameInventory related to the user
    GameInventory.objects.filter(user_id=user_id).delete()

    # Delete GameMapState related to the user
    GameMapState.objects.filter(user_id=user_id).delete()

    # Delete GameUpdateQueue related to the user
    GameUpdateQueue.objects.filter(user_id=user_id).delete()

    # Delete GameElementLookup related to the user
    GameElementLookup.objects.filter(user_id=user_id).delete()

    # Delete GameState related to the user
    GameState.objects.filter(user_id=user_id).delete()

    # Optionally delete other related objects
    # GameEvent.objects.filter(user_id=user_id).delete()
    # Add more deletions if there are other models related to the user


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

        # Delete all related objects before creating a new game
        delete_user_related_objects(user_id)

        game_update, _ = GameUpdateQueue.objects.get_or_create(
            user_id=user_id, defaults={"level": 1, "status": "started"}
        )

        # add a default unarmed item to the user's inventory
        item_generator = ItemGenerator()
        unarmed_item = item_generator.generate_unarmed_item()
        GameInventory.objects.create(
            user_id=user_id,
            item_id=unarmed_item["item_id"],
            map_id=uuid.UUID(int=0),
            item_details=unarmed_item,
        )

        # add the item to the lookup table
        GameElementLookup.objects.create(
            element_id=unarmed_item["item_id"], user_id=user_id
        )

        game_update.status = "started"
        game_update.save()

        try:
            logger.info(f"Validated data before save: {serializer.validated_data}")

            # Ensure map_id defaults to uuid.UUID(int=0) if not provided
            if "map_id" not in serializer.validated_data:
                serializer.validated_data["map_id"] = uuid.UUID(int=0)

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
