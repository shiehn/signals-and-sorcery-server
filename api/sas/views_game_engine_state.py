import uuid

from django.db import transaction
from rest_framework import generics
from game_engine.api.item_generator import ItemGenerator
from game_models.models import (
    GameState,
    GameInventory,
    GameMap,
    GameUpdateQueue,
    GameMapState,
)
from game_engine.api.level_up import level_up
from game_engine.rpg_chat_service import RPGChatService
from .serializers import GameStateSerializer
import logging
from game_models.models import GameElementLookup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user:
            # Add user_id to the validated_data before saving
            serializer.validated_data["user_id"] = user.id

            # Continue with your existing logic
            open_ai_key = self.kwargs.get("open_ai_key")
            logger = logging.getLogger(__name__)

            if open_ai_key:
                logger.info(f"OpenAI Key: {open_ai_key}")
            else:
                logger.error("No OpenAI Key provided")
                raise ValueError("No OpenAI Key provided")

            delete_user_related_objects(user.id)
            item_generator = ItemGenerator()
            unarmed_item = item_generator.generate_unarmed_item()

            GameInventory.objects.create(
                user_id=user.id,
                item_id=unarmed_item["item_id"],
                map_id=uuid.UUID(int=0),
                item_details=unarmed_item,
            )
            GameElementLookup.objects.create(
                element_id=unarmed_item["item_id"], user_id=user.id
            )
            game_update, _ = GameUpdateQueue.objects.get_or_create(
                user_id=user.id, defaults={"level": 1, "status": "started"}
            )

            serializer.save()  # user_id is included in the validated_data
            game_update.status = "queued"
            game_update.save()

            # finally, clear the users chat history if it exits
            rpg_chat_service = RPGChatService()
            rpg_chat_service.clear_chat_history(user.id)

        else:
            logger = logging.getLogger(__name__)
            logger.error("No authenticated user")
            raise PermissionDenied("No authenticated user")


class GameStateDetailView(generics.RetrieveAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the object the view is displaying.
        Overridden to get the game state for the current authenticated user.
        """
        user_id = self.request.user.id  # Get user_id from the authenticated user
        try:
            return GameState.objects.get(
                user_id=user_id
            )  # Adjusted to fetch by user_id
        except GameState.DoesNotExist:
            raise Http404("No GameState matches the given query.")


class GameStateDeleteView(generics.DestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "user_id"


class GameStateUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "id"


class LevelUpView(APIView):
    """
    Level UP the users game
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, environment_id):
        try:
            response = level_up(environment_id)
            return Response(response, status=status.HTTP_200_OK)
        except GameMap.DoesNotExist:
            raise HttpResponseServerError
