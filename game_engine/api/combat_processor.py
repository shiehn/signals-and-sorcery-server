from byo_network_hub.models import GameElementLookup, GameMapState, GameMap, GameState
from game_engine.api.map_inspector import MapInspector

import logging

logger = logging.getLogger(__name__)


class CombatProcessor:
    def attack(self, item_id: str) -> bool:
        logger.info(f"ATTACK WITH ITEM_ID: {item_id}")

        user_id = GameElementLookup.objects.get(element_id=item_id).user_id
        game_state = GameState.objects.get(user_id=user_id)
        map = GameMap.objects.get(id=game_state.map_id).map_graph
        map_inspector = MapInspector(map)
        environment = map_inspector.get_env_by_id(game_state.environment_id)
        encounter_id = environment["game_info"]["encounters"][0]["encounter_id"]

        logger.info(f"ATTACK ENCOUNTER_ID: {encounter_id}")

        elements = [item_id, encounter_id]
        GameMapState.objects.filter(item_id__in=elements).update(consumed=True)

        logger.info(f"ATTACK SUCCESS")

        return True
