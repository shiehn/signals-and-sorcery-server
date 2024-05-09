from rest_framework import status, views
from rest_framework.response import Response
from game_engine.rpg_chat_service import RPGChatService
from byo_network_hub.models import GameState, GameMap
from game_engine.api.map_inspector import MapInspector

import logging

logger = logging.getLogger(__name__)


def handle_message(message: str, token: str):
    # This function should be called by the game engine to handle the user message
    # The game engine should pass the message
    return handle_user_message(message, token)


class GameQueryView(views.APIView):
    authentication_classes = []  # Disables authentication
    permission_classes = []  # Disables permission

    def post(self, request, *args, **kwargs):
        # Extract data from the request body
        token = request.data.get("token")
        query = request.data.get("query")

        if not token or not query:
            # If either token or query is missing, return a bad request response
            return Response(
                {"error": "Both 'token' and 'query' are required in the request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # START -- CRAFTING  THE QUERY
        # Get the game state for the user
        game_state = GameState.objects.get(user_id=token)
        map = GameMap.objects.get(id=game_state.map_id).map_graph
        map_inspector = MapInspector(map)
        environment = map_inspector.get_env_by_id(game_state.environment_id)

        logger.info(f"Environment: {environment['game_info']}")

        # append user context and state to the query
        query = f"{query} user_id={token} environment_id={game_state.environment_id} doors={environment['game_info']['doors']} items={[item['item_id'] for item in environment['game_info']['items']]}"
        # END -- CRAFTING  THE QUERY

        rpg_chat_service = RPGChatService()  # Get the singleton instance
        response = rpg_chat_service.ask_question(token, query)

        return Response({"response": response}, status=status.HTTP_200_OK)
