import logging

from rest_framework import views, status
from rest_framework.response import Response
from byo_network_hub.models import GameElementLookup, GameMapState, GameMap, GameState
from game_engine.api.map_inspector import MapInspector


logger = logging.getLogger(__name__)


class GameNavigateToView(views.APIView):
    def navigate(self, environment_id):
        user_id = GameElementLookup.objects.get(element_id=environment_id).user_id

        game_state = GameState.objects.get(user_id=user_id)

        current_env_id = game_state.environment_id

        map_id = game_state.map_id

        # game_map_state = GameMapState.objects.get(user_id=user_id)

        # map_id = game_map_state.map_id

        map = GameMap.objects.get(id=map_id).map_graph

        map_inspector = MapInspector(map)

        adjacent_env_ids = map_inspector.get_adjacent_environments(str(current_env_id))

        if str(environment_id) in adjacent_env_ids:
            game_state.environment_id = str(environment_id)
            game_state.save()
            return True

    def get(self, request, user_id, environment_id):
        self.navigate(environment_id)

        return Response(
            {
                "message": f"User successfully navigated to environment: {environment_id}"
            },
            status=status.HTTP_200_OK,
        )


class GameNavigateGetAdjacentView(views.APIView):
    def get(self, request, user_id, environment_id):
        try:
            game_state = GameState.objects.get(user_id=user_id)

            map_id = game_state.map_id

            logger.info(f"STEVE - MAP ID: {map_id}")

            map = GameMap.objects.get(id=map_id).map_graph

            logger.info(f"STEVE - MAP: {map}")

            map_inspector = MapInspector(map)

            logger.info(f"STEVE - ENVIRONMENT ID: {environment_id}")

            adjacent_env_ids = map_inspector.get_adjacent_environments(
                str(environment_id)
            )

            logger.info(f"STEVE - ADJACENT ENVIRONMENT IDS: {adjacent_env_ids}")

            return Response(
                {"message": f"{adjacent_env_ids}"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"STEVE - ERROR: {e}")
            return Response(
                {"message": f"Error: {e}"}, status=status.HTTP_500_BAD_REQUEST
            )
