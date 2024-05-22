# Define custom tools with proper arguments and descriptions
from langchain_core.tools import BaseTool

from game_engine.api.environment import get_environment
from game_engine.api.combat_processor import CombatProcessor
from byo_network_hub.models import GameElementLookup


class Combat(BaseTool):
    name = "AttackEncounter"
    description = "This tool takes an item_id and attacks an encounter with it.  It will calculate the damage done by the user's item to the encounter.  It will return the return the combat stats and if the encounter was defeated or not."

    def _run(self, item_id: str):
        combat = CombatProcessor()
        return combat.attack(item_id)

    def _arun(self, item_id: str):
        return self._run(item_id)
