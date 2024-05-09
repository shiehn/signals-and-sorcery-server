from game_engine.api.map_inspector import MapInspector
from byo_network_hub.models import GameMap, GameState, GameElementLookup

import logging

logger = logging.getLogger(__name__)


def get_environment(environment_id, user_id):
    map_id = GameState.objects.get(user_id=user_id).map_id
    map = GameMap.objects.get(id=map_id).map_graph

    map_inspector = MapInspector(map)

    environment = map_inspector.get_env_by_id(environment_id)

    return environment


def navigate_environment(environment_id):
    user_id = GameElementLookup.objects.get(element_id=environment_id).user_id

    logger.info(f"NAV_DEBUG - USER ID: {user_id}")

    game_state = GameState.objects.get(user_id=user_id)

    logger.info(f"NAV_DEBUG - GAME STATE: {game_state}")

    current_env_id = game_state.environment_id

    logger.info(f"NAV_DEBUG - CURRENT ENV ID: {current_env_id}")

    map_id = game_state.map_id

    logger.info(f"NAV_DEBUG - MAP ID: {map_id}")

    map = GameMap.objects.get(id=map_id).map_graph

    logger.info(f"NAV_DEBUG - MAP: {map}")

    map_inspector = MapInspector(map)

    adjacent_env_ids = map_inspector.get_adjacent_environments(str(current_env_id))

    logger.info(f"NAV_DEBUG - environment_id={str(environment_id)}")
    if str(environment_id) in adjacent_env_ids:
        logger.info(f"NAV_DEBUG - IS_ADJACENT user_id={user_id}")

        game_state = GameState.objects.filter(user_id=str(user_id)).first()

        logger.info(f"NAV_DEBUG - GameState.object: {game_state}")

        game_state.environment_id = str(environment_id)
        env = map_inspector.get_env_by_id(str(environment_id))

        logger.info(f"NAV_DEBUG - env: {env}")

        game_state.environment_img = env["game_info"]["environment"]["aesthetic"][
            "image"
        ]

        logger.info(f"NAV_DEBUG - GAME STATE: {game_state}")
        game_state.save()
        return True

    return False
