from langchain_core.tools import BaseTool

from game_engine.api.item import get_item
from game_engine.api.storage import list_items, add_item

from game_engine.api.environment import navigate_environment


class NavigateEnvironment(BaseTool):
    name = "NavigateEnvironment"
    description = "Update the user's current environment to a provided adjacent_environment_id. This tool takes one parameter, adjacent_environment_id not the current environment_id. It returns 'success' if the user successfully navigated to the new environment, otherwise a message."

    def _run(self, adjacent_environment_id: str) -> str:
        return navigate_environment(adjacent_environment_id)

    def _arun(self, adjacent_environment_id: str) -> str:
        return self._run(adjacent_environment_id)
