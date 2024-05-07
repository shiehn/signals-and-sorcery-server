from game_engine.api.map_inspector import MapInspector
from byo_network_hub.models import GameMap, GameState, GameElementLookup


def get_environment(environment_id, user_id):
    map_id = GameState.objects.get(user_id=user_id).map_id
    map = GameMap.objects.get(id=map_id).map_graph

    map_inspector = MapInspector(map)

    environment = map_inspector.get_env_by_id(environment_id)

    return environment


def navigate_environment(environment_id):
    user_id = GameElementLookup.objects.get(element_id=environment_id).user_id

    game_state = GameState.objects.get(user_id=user_id)

    current_env_id = game_state.environment_id

    map_id = game_state.map_id

    map = GameMap.objects.get(id=map_id).map_graph

    map_inspector = MapInspector(map)

    adjacent_env_ids = map_inspector.get_adjacent_environments(str(current_env_id))

    if str(environment_id) in adjacent_env_ids:
        game_state.environment_id = str(environment_id)
        game_state.environment_img = map_inspector.get_env_by_id(
            environment_id
        ).aesthetic.image
        game_state.save()
        return True
