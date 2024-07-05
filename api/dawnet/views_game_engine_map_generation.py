from rest_framework.response import Response
from rest_framework import status, views
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from byo_network_hub.models import GameMap
from .serializers import GameMapSerializer
from rest_framework.permissions import IsAuthenticated


class GameMapGeneration(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        level = int(request.query_params.get("level"))
        asset_desc = request.query_params.get("asset_desc")

        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=level + 2, percent_connected=0.25
        ).get_json()

        processed_map = MapProcessor(unprocessed_map)
        processed_map = processed_map.add_entrance_exit()
        processed_map = processed_map.add_items()
        processed_map = processed_map.add_encounters()

        map = processed_map.get_map()

        # Create the GameMap object and save it to the database
        gamemap = GameMap.objects.create(
            level=level, description=asset_desc, map_graph=map
        )

        # Serialize the newly created GameMap object
        serializer = GameMapSerializer(gamemap)

        # EventPublisher().publish(user_id, "level-up-complete", {})

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
