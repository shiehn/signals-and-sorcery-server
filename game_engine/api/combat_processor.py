from byo_network_hub.models import GameElementLookup, GameMapState, GameMap, GameState
from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.event_publisher import EventPublisher

import logging

logger = logging.getLogger(__name__)


class CombatProcessor:
    def attack(self, item_id: str) -> bool:
        logger.info(f"ATTACK WITH ITEM_ID: {item_id}")

        user_id = GameElementLookup.objects.get(element_id=item_id).user_id
        game_state = GameState.objects.get(user_id=user_id)
        map = GameMap.objects.get(id=game_state.map_id).map_graph

        game_map_state = GameMapState.objects.filter(map_id=game_state.map_id).first()

        if game_map_state is not None and len(game_map_state) > 0:
            map_filter = MapStateFilter(map)
            filtered_map = map_filter.filter(game_map_state)
            map_inspector = MapInspector(filtered_map)
        else:
            map_inspector = MapInspector(map)

        environment = map_inspector.get_env_by_id(game_state.environment_id)
        encounter_id = environment["game_info"]["encounters"][0]["encounter_id"]

        logger.info(f"ATTACK ENCOUNTER_ID: {encounter_id}")

        elements = [item_id, encounter_id]
        GameMapState.objects.filter(item_id__in=elements).update(consumed=True)

        # FIRED EVENT
        EventPublisher().publish(user_id, "encounter-victory")
        # FIRED EVENT
        # encounter-victory
        # encounter-loss

        logger.info(f"ATTACK SUCCESS")

        return True
