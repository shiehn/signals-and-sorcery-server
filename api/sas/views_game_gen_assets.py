from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from game_models.models import GameState, GameMap
import logging
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator
from game_models.models import GameUpdateQueue, GameElementLookup
from django.db import transaction
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from game_engine.api.map_inspector import MapInspector
from game_engine.api.event_publisher import EventPublisher
from asgiref.sync import sync_to_async, async_to_sync
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def add_uuids_to_lookup(user_id, uuids):
    with transaction.atomic():  # Start a new transaction
        for uuid in uuids:
            GameElementLookup.objects.create(element_id=uuid, user_id=user_id)


class AssetGenerateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_id = request.user.id
        open_ai_key = request.data.get(
            "api_key"
        )  # Continue extracting API key from request data

        if not open_ai_key or open_ai_key in ["", "placeholder_key"]:
            return Response(
                {"error": "Invalid or missing OpenAI Key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return async_to_sync(self.async_post)(user_id, open_ai_key)

    async def async_post(self, user_id, open_ai_key):
        logger = logging.getLogger(__name__)

        try:
            game_state = await sync_to_async(GameState.objects.get)(user_id=user_id)
        except GameState.DoesNotExist:
            raise NotFound("GameState not found")

        if not open_ai_key:
            raise ValueError("No OpenAI Key provided")

        asset_generator = AssetGenerator(open_ai_key=open_ai_key)

        aesthetic = game_state.aesthetic
        art_style = game_state.art_style

        game_setting = await asset_generator.generate_politics_and_history(aesthetic)
        game_state.setting = game_setting

        game_update = await sync_to_async(GameUpdateQueue.objects.get)(user_id=user_id)

        # Set game update status to "started"
        game_update.status = "started"
        await sync_to_async(game_update.save)()

        # GENERATE THE MAP
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=int(game_update.level) + 2, percent_connected=0.25
        ).get_json()

        processed_map = MapProcessor(unprocessed_map)
        processed_map = processed_map.add_entrance_exit()
        processed_map = processed_map.add_items()
        processed_map = processed_map.add_encounters()

        map = processed_map.get_map()

        game_map = await sync_to_async(GameMap.objects.create)(
            level=game_update.level,
            description=aesthetic + " " + art_style,
            map_graph=map,
        )

        map_inspector = MapInspector(map)
        uuids = map_inspector.extract_uuids()
        await sync_to_async(add_uuids_to_lookup)(user_id, uuids)

        entrance_env_id = map_inspector.get_env_id_of_entrance()
        entrance_env_img = map_inspector.get_env_by_id(entrance_env_id)["game_info"][
            "environment"
        ]["aesthetic"]["image"]

        logger.info(f"Calculated environment_id: {entrance_env_id}")
        logger.info(f"Calculated environment_img: {entrance_env_img}")

        game_state.map_id = game_map.id
        game_state.environment_id = entrance_env_id
        game_state.environment_img = entrance_env_img

        try:
            asset_generator = AssetGenerator(open_ai_key=open_ai_key)
            aesthetic_generator = AestheticGenerator(
                aesthetic=aesthetic,
                art_style=art_style,
                setting=game_setting,
                map=game_map.map_graph,
                asset_generator=asset_generator,
            )
            map = await aesthetic_generator.add_all_aesthetics()

            game_map.map_graph = map
            await sync_to_async(game_map.save)()

            game_state.map_id = game_map.id
            await sync_to_async(game_state.save)()

            # Set game update status to "completed"
            game_update.status = "completed"
            await sync_to_async(game_update.save)()

            await EventPublisher().publish_async(user_id, "level-up-complete", {})

            return Response({"status": "Assets generated successfully"})

        except Exception as e:
            logger.error(f"Error during asset generation: {str(e)}")

            # Set game update status to "error"
            game_update.status = "error"
            await sync_to_async(game_update.save)()

            return Response({"error": str(e)}, status=500)
