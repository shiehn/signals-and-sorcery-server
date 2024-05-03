from rest_framework import views, status
from rest_framework.response import Response
from byo_network_hub.models import GameElementLookup, GameMapState, GameMap
from game_engine.api.map_inspector import MapInspector


class GameNavigateToView(views.APIView):
    def navigate(self, environment_id):
        user_id = GameElementLookup.objects.get(environment_id=environment_id).user_id

        current_env_id = GameMapState.objects.get(user_id=user_id).environment_id

        game_map_state = GameMapState.objects.get(user_id=user_id)

        map_id = game_map_state.map_id

        map = GameMap.objects.get(id=map_id).map_graph

        map_inspector = MapInspector(map)

        adjacent_env_ids = map_inspector.get_adjacent_environments(current_env_id)

        if environment_id in adjacent_env_ids:
            game_map_state.environment_id = environment_id
            game_map_state.save()
            return True

        # confirm that the target environment_id is a valid move from the current environment_id

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
        game_map_state = GameMapState.objects.get(user_id=user_id)

        map_id = game_map_state.map_id

        map = GameMap.objects.get(id=map_id).map_graph

        map_inspector = MapInspector(map)

        adjacent_env_ids = map_inspector.get_adjacent_environments(environment_id)

        return Response({"message": f"{adjacent_env_ids}"}, status=status.HTTP_200_OK)
