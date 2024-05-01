from rest_framework.response import Response
from rest_framework import status, views
from game_engine.api.generator import MapGenerator


class GameMapGeneration(views.APIView):
    authentication_classes = []  # Disables authentication
    permission_classes = []  # Disables permission

    def get(self, request, *args, **kwargs):
        level = int(request.query_params.get("level"))
        asset_desc = request.query_params.get(
            "asset_desc"
        )  # Changed from asset_description for consistency

        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=level, percent_connected=0.25
        ).get_json()

        return Response(
            {"level": level, "asset_desc": asset_desc, "map_graph": unprocessed_map},
            status=status.HTTP_200_OK,
        )
