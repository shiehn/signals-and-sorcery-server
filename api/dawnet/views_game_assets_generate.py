from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from byo_network_hub.models import GameState, GameMap
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator
from game_engine.api.event_publisher import EventPublisher  # Import EventPublisher
from asgiref.sync import sync_to_async
from rest_framework.permissions import IsAuthenticated


class GameAssetsGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    async def post(self, request, user_id):

        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        api_key = request.data.get("api_key")  # Extract API

        logger.info("BBB *******************************")
        logger.info(f"BBB API_KEY: {api_key}")
        logger.info("BBB *******************************")
        # Accessing aesthetic description from the POST data
        aesthetic = request.data.get("aesthetic")
        if not aesthetic:
            return Response(
                {"message": "Aesthetic description is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            game_state = await sync_to_async(GameState.objects.get)(
                user_id=str(user_id)
            )
            map_id = game_state.map_id
            game_map_db = await sync_to_async(GameMap.objects.get)(id=map_id)
            map = game_map_db.map_graph

            asset_generator = AssetGenerator(open_ai_key="OPEN_AI_KEY")
            aesthetic_generator = AestheticGenerator(
                aesthetic=aesthetic, map=map, asset_generator=asset_generator
            )

            updated_map = await aesthetic_generator.add_all_aesthetics()

            game_map_db.map_graph = updated_map
            await sync_to_async(game_map_db.save)()

            event_publisher = EventPublisher()
            await event_publisher.publish(
                user_id, "assets_generated", {"map_id": map_id}
            )

            return Response({"message": "Success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
