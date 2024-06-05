from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.event_publisher import EventPublisher
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
    try:
        user_id = GameElementLookup.objects.get(element_id=environment_id).user_id
        logger.info(f"LEVEL_UP_DEBUG - USER ID: {user_id}")

        game_state = GameState.objects.filter(user_id=user_id).first()
        map_id = game_state.map_id
        current_env_id = game_state.environment_id
        game_map = GameMap.objects.get(id=map_id).map_graph
        game_map_states = list(GameMapState.objects.filter(map_id=map_id))

        map_inspector = MapInspector(
            game_map
            if not game_map_states
            else MapStateFilter(game_map).filter(game_map_states)
        )
        env_exit_id = map_inspector.get_env_id_of_exit()

        logger.info(
            f"LEVEL_UP_DEBUG - environment_id: {environment_id}, current_env_id: {current_env_id}, env_exit_id: {env_exit_id}"
        )

        if str(current_env_id) == str(env_exit_id):
            logger.info("LEVEL_UP_DEBUG - IDs match!")
            game_state.level += 1
            game_state.save(update_fields=["level"])

            # FIRED LEVEL_UP EVENT
            # FIRED LEVEL_UP EVENT
            EventPublisher().publish(user_id, "level-up-complete")
            # FIRED LEVEL_UP EVENT
            # FIRED LEVEL_UP EVENT

            game_update_queue, created = GameUpdateQueue.objects.get_or_create(
                user_id=user_id,
                defaults={"level": game_state.level, "status": "pending"},
            )
            if not created:
                logger.info("LEVEL_UP_DEBUG - New Queue")
                game_update_queue.level = game_state.level
                game_update_queue.status = "queued"
                game_update_queue.save()
            else:
                logger.info("LEVEL_UP_DEBUG - UPDATED")

            logger.info(f"Game level updated to {game_state.level} for user {user_id}")
            return {"message": "success"}

        return {"message": "There was an error while attempting to level up"}
    except Exception as e:
        logger.error(f"Error during level up: {str(e)}")
        return {"message": "An exception occurred while attempting to level up"}
