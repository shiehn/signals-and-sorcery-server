# Define custom tools with proper arguments and descriptions
from langchain_core.tools import BaseTool

from game_engine.api.level_up import level_up


# Level up TOOLS


class LevelUp(BaseTool):
    name = "LevelUp"
    description = (
        "When a player has reach the exit location of a map they have the "
        "option to level up with this tool.  The level up method takes an "
        "environment_id as a parameter"
    )

    def _run(self, environment_id: str):
        response = level_up(environment_id=environment_id)

        return response

    def _arun(self, environment_id: str):
        return self._run(environment_id)
