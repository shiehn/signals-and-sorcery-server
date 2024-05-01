from rest_framework import generics
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from byo_network_hub.models import GameState, GameMap
from .serializers import GameStateSerializer


class GameStateCreateView(generics.CreateAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer

    def perform_create(self, serializer):
        user_id = serializer.validated_data["user_id"]
        level = serializer.validated_data["level"]
        aesthetic = serializer.validated_data["aesthetic"]

        # GENERATE A NEW MAP
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=int(level) + 2, percent_connected=0.25
        ).get_json()

        processed_map = MapProcessor(unprocessed_map)
        processed_map = processed_map.add_entrance_exit()
        processed_map = processed_map.add_items()
        processed_map = processed_map.add_encounters()

        map = processed_map.get_map()
        # Create the GameMap object and save it to the database
        game_map = GameMap.objects.create(
            level=level, description=aesthetic, map_graph=map
        )

        # Set the map_id in the validated_data before saving
        serializer.validated_data["map_id"] = game_map.id

        # Save the instance with the new map_id
        serializer.save()


class GameStateDetailView(generics.RetrieveAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "user_id"


class GameStateDeleteView(generics.DestroyAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "id"


class GameStateUpdateView(generics.UpdateAPIView):
    queryset = GameState.objects.all()
    serializer_class = GameStateSerializer
    lookup_field = "id"
