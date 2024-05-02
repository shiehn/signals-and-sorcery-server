from rest_framework import views, status
from rest_framework.response import Response
from .serializers import GameInventorySerializer
from byo_network_hub.models import (
    GameInventory,
)


class InventoryListView(views.APIView):
    """
    View to list all items in a user's inventory.
    """

    def get(self, request, user_id):
        inventory_items = GameInventory.objects.filter(user_id=user_id)
        serializer = GameInventorySerializer(inventory_items, many=True)
        return Response(serializer.data)


class InventoryCreateView(views.APIView):
    """
    View to add a new item to the user's inventory.
    """

    def post(self, request, user_id):
        data = request.data
        data["user_id"] = user_id  # Set user_id from URL to the data
        serializer = GameInventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
