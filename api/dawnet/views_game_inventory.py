from rest_framework import views, status
from django.db.models import Q
import uuid
from rest_framework.response import Response
from .serializers import GameInventorySerializer
from byo_network_hub.models import GameInventory
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class InventoryListView(views.APIView):
    """
    View to list all items in a user's inventory.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):

        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        inventory_items = GameInventory.objects.filter(user_id=user_id)
        if not inventory_items.exists():
            return Response(
                {"error": "User does not have any items in the inventory"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = GameInventorySerializer(inventory_items, many=True)
        return Response(serializer.data)


class InventoryCreateView(views.APIView):
    """
    View to add a new item to the user's inventory.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        data = request.data
        data["user_id"] = str(user_id)  # Set user_id from URL to the data
        serializer = GameInventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
