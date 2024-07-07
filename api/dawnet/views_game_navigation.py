import logging

from rest_framework import views, status
from rest_framework.response import Response
from byo_network_hub.models import GameElementLookup, GameMapState, GameMap, GameState
from game_engine.api.map_inspector import MapInspector
from game_engine.api.environment import navigate_environment
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


logger = logging.getLogger(__name__)


class GameNavigateToView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, environment_id):

        res = navigate_environment(str(environment_id))

        if res != "success":
            return Response(
                {
                    "message": f"User unable to navigate to environment: {environment_id}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": f"User successfully navigated to environment: {environment_id}"
            },
            status=status.HTTP_200_OK,
        )


class GameNavigateGetAdjacentView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, environment_id):

        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        try:
            game_state = GameState.objects.get(user_id=str(user_id))

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
