from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from byo_network_hub.models import GameState, GameMap
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator


class GameAssetsGenerateView(APIView):
    def post(self, request, user_id):
        # Accessing aesthetic description from the POST data
        aesthetic = request.data.get("aesthetic")
        if not aesthetic:
            return Response(
                {"message": "Aesthetic description is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            game_state = GameState.objects.get(user_id=str(user_id))
            map_id = game_state.map_id
            game_map_db = GameMap.objects.get(id=map_id)
            map = game_map_db.map_graph

            asset_generator = AssetGenerator(open_ai_key="OPEN_AI_KEY")
            aesthetic_generator = AestheticGenerator(
                aesthetic=aesthetic, map=map, asset_generator=asset_generator
            )

            # updated_map = await aesthetic_generator.add_all_aesthetics()

            updated_map = aesthetic_generator.add_all_aesthetics()

            game_map_db.map_graph = updated_map
            game_map_db.save()

            return Response({"message": "Success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
