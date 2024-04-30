from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import JSONParser
from byo_network_hub.models import GameMap
from .serializers import GameMapSerializer


class GameMapView(APIView):
    """
    Retrieve or update a specific GameMap instance.
    """

    def get_object(self, uuid):
        try:
            return GameMap.objects.get(pk=uuid)
        except GameMap.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        gamemap = self.get_object(uuid)
        serializer = GameMapSerializer(gamemap)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid, format=None):
        gamemap = self.get_object(uuid)
        serializer = GameMapSerializer(gamemap, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameMapCreateView(APIView):
    """
    Create a new GameMap instance.
    """

    def post(self, request, format=None):
        serializer = GameMapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
