from byo_network_hub.models import GameMapState
from .serializers import GameMapStateSerializer


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class GameMapStateViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = GameMapStateSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        map_id = self.request.query_params.get("map_id")
        if user_id is not None and map_id is not None:
            return GameMapState.objects.filter(user_id=user_id, map_id=map_id)
        return GameMapState.objects.none()  # Return an empty queryset

    def perform_create(self, serializer):
        serializer.save()  # This will use the validated data from the request to save the new instance
