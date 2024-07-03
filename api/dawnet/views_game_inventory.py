from rest_framework import views, status
from django.db.models import Q
import uuid
from rest_framework.response import Response
from .serializers import GameInventorySerializer
from byo_network_hub.models import GameInventory, GameState, GameMapState


class InventoryListView(views.APIView):
    """
    View to list all items in a user's inventory.
    """

    def get(self, request, user_id):

        inventory_items = GameInventory.objects.filter(user_id=user_id)
        if not inventory_items.exists():
            return Response(
                {"error": "User does not have any items in the inventory"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # try:
        #     game_state = GameState.objects.get(user_id=user_id)
        # except GameState.DoesNotExist:
        #     return Response(
        #         {"error": "User does not have a game state"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )
        #
        # game_map_states = GameMapState.objects.filter(map_id=game_state.map_id)
        # consumed_item_ids = {
        #     state.item_id for state in game_map_states if state.consumed
        # }
        #
        # inventory_items = (
        #     GameInventory.objects.filter(user_id=user_id)
        #     .filter(Q(map_id=game_state.map_id) | Q(map_id=uuid.UUID(int=0)))
        #     .exclude(item_id__in=consumed_item_ids)
        # )
        #
        # if not inventory_items.exists():
        #     return Response(
        #         {"error": "User does not have any items in the inventory"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )

        serializer = GameInventorySerializer(inventory_items, many=True)
        return Response(serializer.data)


class InventoryCreateView(views.APIView):
    """
    View to add a new item to the user's inventory.
    """

    def post(self, request, user_id):
        data = request.data
        data["user_id"] = str(user_id)  # Set user_id from URL to the data
        serializer = GameInventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
