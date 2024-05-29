from rest_framework import status, views
from rest_framework.response import Response
from game_engine.rpg_chat_service import RPGChatService
from byo_network_hub.models import GameState, GameMap, GameMapState
from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter

import logging
import re

logger = logging.getLogger(__name__)


# def handle_message(message: str, token: str):
#     # This function should be called by the game engine to handle the user message
#     # The game engine should pass the message
#     return handle_user_message(message, token)


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
        action = {"encounter": None}

        if not token or not query:
            # If either token or query is missing, return a bad request response
            return Response(
                {"error": "Both 'token' and 'query' are required in the request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # START -- CRAFTING  THE QUERY
        # Get the game state for the user
        game_state = GameState.objects.get(user_id=token)
        logger.info(f"XXX GAME_STATE: {game_state}")

        map_id = game_state.map_id
        map = GameMap.objects.get(id=map_id).map_graph
        game_map_states = list(GameMapState.objects.filter(map_id=map_id))

        if game_map_states is not None and len(game_map_states) > 0:
            map_filter = MapStateFilter(map)
            filtered_map = map_filter.filter(game_map_states)
            map_inspector = MapInspector(filtered_map)
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

        # append user context and state to the query
        query = f"{query} user_id={token} environment_id={game_state.environment_id} doors={environment['game_info']['doors']} items={[item['item_id'] for item in environment['game_info']['items']]}"
        # END -- CRAFTING  THE QUERY

        rpg_chat_service = RPGChatService()  # Get the singleton instance
        response = rpg_chat_service.ask_question(token, query)

        filtered_response = strip_patterns(response)

        return Response(
            {"response": filtered_response, "action": action}, status=status.HTTP_200_OK
        )
