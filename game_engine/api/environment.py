from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.event_publisher import EventPublisher
from byo_network_hub.models import GameMap, GameState, GameElementLookup, GameMapState

import logging

logger = logging.getLogger(__name__)


def create_encounter_start_event(encounters):
    combat_stats = {
        "phase": "encounter-start",
        "encounter": encounters[0]["encounter_level"],
        "chance_of_success_base": 100 - (encounters[0]["encounter_level"] * 10),
    }
    return combat_stats


def get_environment(environment_id, user_id):
    map_id = GameState.objects.get(user_id=user_id).map_id
    map = GameMap.objects.get(id=map_id).map_graph

    game_map_states = list(GameMapState.objects.filter(map_id=map_id))

    if game_map_states is not None and len(game_map_states) > 0:
        map_filter = MapStateFilter(map)
        filtered_map = map_filter.filter(game_map_states)
        map_inspector = MapInspector(filtered_map)
    else:
        map_inspector = MapInspector(map)

    environment = map_inspector.get_env_by_id(str(environment_id))

    env_exit_id = map_inspector.get_env_id_of_exit()
    if str(environment_id) == str(env_exit_id):
        # FIRED ENCOUNTER EVENT
        EventPublisher().publish(user_id, "level-up-ready")

    if (
        environment["game_info"]["encounters"] is not None
        and len(environment["game_info"]["encounters"]) > 0
    ):
        environment["message"] = "You must deal with the encounter!"
        # FIRED ENCOUNTER EVENT
        # FIRED ENCOUNTER EVENT

        combat_stats = create_encounter_start_event(
            environment["game_info"]["encounters"]
        )
        EventPublisher().publish(user_id, "encounter-start", combat_stats)
        # FIRED ENCOUNTER EVENT
        # FIRED ENCOUNTER EVENT

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

    # map_inspector = MapInspector(map)
    game_map_states = list(GameMapState.objects.filter(map_id=map_id))

    if game_map_states is not None and len(game_map_states) > 0:
        map_filter = MapStateFilter(map)
        filtered_map = map_filter.filter(game_map_states)
        map_inspector = MapInspector(filtered_map)
    else:
        map_inspector = MapInspector(map)

    current_env = map_inspector.get_env_by_id(str(current_env_id))

    env_exit_id = map_inspector.get_env_id_of_exit()
    if str(current_env_id) == str(env_exit_id):
        # FIRED ENCOUNTER EVENT
        EventPublisher().publish(user_id, "level-up-ready")

    if (
        current_env["game_info"]["encounters"] is not None
        and len(current_env["game_info"]["encounters"]) > 0
    ):
        # FIRED ENCOUNTER EVENT
        combat_stats = create_encounter_start_event(
            current_env["game_info"]["encounters"]
        )
        EventPublisher().publish(user_id, "encounter-start", combat_stats)
        return "You must deal with the encounter!"

    logger.info(f"NAV_DEBUG - CURRENT ENV: {current_env}")

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
        return "success"

    return "Error"
