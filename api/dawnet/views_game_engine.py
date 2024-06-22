# views_game_engine.py

from rest_framework import status, views
from rest_framework.response import Response
from game_engine.rpg_chat_service import RPGChatService
from byo_network_hub.models import GameState, GameMap, GameMapState
from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.storage import list_items
import logging
import re

logger = logging.getLogger(__name__)


def strip_patterns(text):
    # Pattern to match UUIDs in parentheses
    uuid_pattern = re.compile(r"\(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\)")
    # Pattern to match markdown-style image URLs
    markdown_url_pattern = re.compile(r"!\[.*?\]\(https:\/\/[^\)]+\)")

    # Removing UUIDs in parentheses
    text = re.sub(uuid_pattern, "", text)
    # Removing markdown-style image URLs
    text = re.sub(markdown_url_pattern, "", text)

    return text


class GameQueryView(views.APIView):
    authentication_classes = []  # Disables authentication
    permission_classes = []  # Disables permission

    def post(self, request, *args, **kwargs):
        # Extract data from the request body
        token = request.data.get("token")
        query = request.data.get("query")
        api_key = request.data.get("api_key")  # Extract API key

        logger.info("AAA *******************************")
        logger.info(f"AAA TOKEN: {token}")
        logger.info(f"AAA QUERY: {query}")
        logger.info(f"AAA API_KEY: {api_key}")
        logger.info("AAA *******************************")

        action = {"encounter": None}

        if not token or not query or not api_key:  # Check if api_key is provided
            # If either token, query or api_key is missing, return a bad request response
            return Response(
                {
                    "error": "Both 'token', 'query', and 'api_key' are required in the request body"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # START -- CRAFTING THE QUERY
        # Get the game state for the user
        game_state = GameState.objects.get(user_id=token)
        logger.info(f"XXX GAME_STATE: {game_state}")

        map_id = game_state.map_id
        map = GameMap.objects.get(id=map_id).map_graph
        logger.info(f"XXX GAME_MAP: {map}")
        game_map_states = list(GameMapState.objects.filter(map_id=map_id))

        if game_map_states is not None and len(game_map_states) > 0:
            map_filter = MapStateFilter(map)
            filtered_map = map_filter.filter(game_map_states)
            map_inspector = MapInspector(filtered_map)

            logger.info(f"XXX GAME_FILTERED_MAP: {filtered_map}")
        else:
            map_inspector = MapInspector(map)

        environment = map_inspector.get_env_by_id(game_state.environment_id)
        logger.info(f"XXX ENVIRONMENT: {environment}")

        # handle potential encounters
        if (
            environment["game_info"]["encounters"] is not None
            and len(environment["game_info"]["encounters"]) > 0
        ):
            action["encounter"] = environment["game_info"]["encounters"][0]

        # Get the user's items
        inventory_items = list_items(token)

        # Extract item IDs from inventory items
        inventory_item_ids = [item.item_id for item in inventory_items]

        # Ensure inventory_items is a list of objects with item_id attribute
        inventory_item_ids = [str(item.item_id) for item in inventory_items]

        # append user context and state to the query
        query = (
            f"{query} user_id={token} environment_id={game_state.environment_id} "
            f"doors={environment['game_info']['doors']} "
            f"environment_items={[item['item_id'] for item in environment['game_info']['items']]} "
            f"inventory_items={inventory_item_ids}"
        )
        # END -- CRAFTING THE QUERY

        rpg_chat_service = RPGChatService()  # Get the singleton instance
        response = rpg_chat_service.ask_question(
            token, query, api_key
        )  # Pass the API key

        filtered_response = strip_patterns(response)

        return Response(
            {"response": filtered_response, "action": action}, status=status.HTTP_200_OK
        )
