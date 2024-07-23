# Define custom tools with proper arguments and descriptions
from langchain_core.tools import BaseTool

from game_engine.api.environment import get_environment
from game_engine.api.combat_processor import CombatProcessor
from game_models.models import GameElementLookup


class Combat(BaseTool):
    name = "AttackEncounter"
    description = "This tool takes an item_id and attacks an encounter with it.  It will calculate the combat results and return either 'encounter-loss', encounter-victory', or 'encounter-error'."

    def _run(self, item_id: str):
        combat = CombatProcessor()
        return combat.attack(item_id)

    def _arun(self, item_id: str):
        return self._run(item_id)
