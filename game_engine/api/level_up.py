from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter
from byo_network_hub.models import (
    GameMap,
    GameState,
    GameElementLookup,
    GameMapState,
    GameUpdateQueue,
)

import logging

logger = logging.getLogger(__name__)


def level_up(environment_id):
    user_id = GameElementLookup.objects.get(element_id=environment_id).user_id

    logger.info(f"LEVEL_UP_DEBUG - USER ID: {user_id}")

    # Retrieve the first GameState object matching the user_id
    game_state = GameState.objects.filter(user_id=user_id).first()
    map_id = game_state.map_id
    current_env_id = game_state.environment_id
    map = GameMap.objects.get(id=map_id).map_graph

    game_map_states = list(GameMapState.objects.filter(map_id=map_id))

    if game_map_states:
        map_filter = MapStateFilter(map)
        filtered_map = map_filter.filter(game_map_states)
        map_inspector = MapInspector(filtered_map)
    else:
        map_inspector = MapInspector(map)

    env_exit_id = map_inspector.get_env_id_of_exit()

    if current_env_id == env_exit_id:
        # Level up
        game_state.level += 1
        game_state.save()

        # Update GameUpdateQueue
        game_update_queue, created = GameUpdateQueue.objects.get_or_create(
            user_id=user_id, defaults={"level": game_state.level, "status": "pending"}
        )
        if not created:
            game_update_queue.level = game_state.level
            game_update_queue.status = "pending"
            game_update_queue.save()

        logger.info(f"Game level updated to {game_state.level} for user {user_id}")
        # TODO: Inform the UI to generate a new map
        return {"message": "success"}

    return {"message": "There was an error while attempting to level up"}
