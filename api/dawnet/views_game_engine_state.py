from django.db import transaction
from rest_framework import generics
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from game_engine.api.map_inspector import MapInspector
from byo_network_hub.models import GameState, GameMap, GameElementLookup
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator
from .serializers import GameStateSerializer
import logging

logger = logging.getLogger(__name__)


GENERATE_ASSETS_ON_GAME_STATE_CREATE = True


def add_uuids_to_lookup(user_id, uuids):
    with transaction.atomic():  # Start a new transaction
        for uuid in uuids:
            GameElementLookup.objects.create(element_id=uuid, user_id=user_id)


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

        if GENERATE_ASSETS_ON_GAME_STATE_CREATE:
            asset_generator = AssetGenerator(open_ai_key="OPEN_AI_KEY")
            aesthetic_generator = AestheticGenerator(
                aesthetic=aesthetic, map=map, asset_generator=asset_generator
            )
            map = aesthetic_generator.add_all_aesthetics()

        # Create the GameMap object and save it to the database
        game_map = GameMap.objects.create(
            level=level, description=aesthetic, map_graph=map
        )

        map_inspector = MapInspector(map)

        # associate all the elements in the map with the user_id
        uuids = map_inspector.extract_uuids()
        add_uuids_to_lookup(user_id, uuids)

        # Set the map_id in the validated_data before saving
        serializer.validated_data["map_id"] = game_map.id

        # Assume the user is starting at the entrance, so set the current_room to the entrance

        entrance_env_id = map_inspector.get_env_id_of_entrance()

        serializer.validated_data["environment_id"] = entrance_env_id

        serializer.validated_data["environment_img"] = map_inspector.get_env_by_id(
            entrance_env_id
        )["game_info"]["environment"]["aesthetic"]["image"]

        # logger.info("DA_HELL " + str(map_inspector.get_env_by_id(entrance_env_id)))

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
