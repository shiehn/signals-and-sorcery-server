from byo_network_hub.models import (
    GameElementLookup,
    GameMapState,
    GameMap,
    GameState,
    GameInventory,
)
from game_engine.api.map_inspector import MapInspector
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.event_publisher import EventPublisher

import logging
import random

logger = logging.getLogger(__name__)


class CombatProcessor:
    def attack_roll(self) -> int:
        return random.randint(1, 100)

    def create_combat_stats(self, encounter, item, roll) -> dict:
        if encounter is None or item is None:
            return {
                "phase": "no-encounter-or-item",
                "encounter": None,
                "modifiers": [],
                "chance_of_success_base": None,
                "chance_of_success_total": None,
                "result": roll,
            }

        base_chance_of_success = 100 - (encounter["encounter_level"] * 10)
        total_chance_of_success = (
            base_chance_of_success + item.item_details["item_level"]
        )  # Access item_level from item_details

        combat_phase = "encounter-loss"
        if roll <= total_chance_of_success:
            combat_phase = "encounter-victory"

        combat_stats = {
            "phase": combat_phase,
            "encounter": encounter["encounter_level"],
            "modifiers": [
                {
                    "item": str(item.item_id),  # Convert UUID to string
                    "modifier": item.item_details[
                        "item_level"
                    ],  # Access item_level from item_details
                },
            ],
            "chance_of_success_base": base_chance_of_success,
            "chance_of_success_total": total_chance_of_success,
            "result": roll,
        }

        return combat_stats

    def attack(self, item_id: str) -> bool:
        logger.info(f"ATTACK WITH ITEM_ID: {item_id}")

        user_id = GameElementLookup.objects.get(element_id=item_id).user_id
        game_state = GameState.objects.get(user_id=user_id)
        map = GameMap.objects.get(id=game_state.map_id).map_graph

        logger.info(f"XXX ATTACK MAP: {map}")

        game_map_state = list(GameMapState.objects.filter(map_id=game_state.map_id))

        if game_map_state is not None:
            map_filter = MapStateFilter(map)
            filtered_map = map_filter.filter(game_map_state)
            map_inspector = MapInspector(filtered_map)
        else:
            map_inspector = MapInspector(map)

        environment = map_inspector.get_env_by_id(game_state.environment_id)

        if (
            environment["game_info"]["encounters"] is None
            or len(environment["game_info"]["encounters"]) == 0
        ):
            return False

        encounter = environment["game_info"]["encounters"][0]
        encounter_id = environment["game_info"]["encounters"][0]["encounter_id"]

        logger.info(f"ATTACK ENCOUNTER_ID: {encounter_id}")

        # lookup the item in the database
        item = GameInventory.objects.get(item_id=item_id)
        roll = self.attack_roll()

        logger.info(f"XYZ item: {item}")

        combat_stats = self.create_combat_stats(encounter, item, roll)

        logger.info(f"ABC COMBAT STATS: {combat_stats}")

        if combat_stats["phase"] == "encounter-victory":
            if item.item_details["item_type"] == "unarmed":
                game_map_state, created = GameMapState.objects.get_or_create(
                    map_id=game_state.map_id,
                    item_id=encounter_id,
                    defaults={"user_id": user_id, "aesthetic": "", "consumed": True},
                )
                if not created:
                    game_map_state.consumed = True
                    game_map_state.save()
                logger.info("ABC 1")
            else:
                elements = [item_id, encounter_id]
                for element_id in elements:
                    game_map_state, created = GameMapState.objects.get_or_create(
                        map_id=game_state.map_id,
                        item_id=element_id,
                        defaults={
                            "user_id": user_id,
                            "aesthetic": "",
                            "consumed": True,
                        },
                    )
                    if not created:
                        game_map_state.consumed = True
                        game_map_state.save()
                logger.info("ABC 2")
        else:
            # in case of loss, only the item is consumed, not the encounter
            if item.item_details["item_type"] == "unarmed":
                # DON'T CONSUME UNARMED ITEM
                logger.info("ABC 3")
            else:
                game_map_state, created = GameMapState.objects.get_or_create(
                    map_id=game_state.map_id,
                    item_id=item_id,
                    defaults={"user_id": user_id, "aesthetic": "", "consumed": True},
                )
                if not created:
                    game_map_state.consumed = True
                    game_map_state.save()
                logger.info("ABC 4")

        EventPublisher().publish(user_id, combat_stats["phase"], combat_stats)

        logger.info("ATTACK SUCCESS")

        return True
