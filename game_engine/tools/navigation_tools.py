from langchain_core.tools import BaseTool

from game_engine.api.item import get_item
from game_engine.api.storage import list_items, add_item

from game_engine.api.environment import navigate_environment


class NavigateEnvironment(BaseTool):
    name = "NavigateEnvironment"
    description = "Update the user's current environment to a provided adjacent environment_id. This tool takes one parameter, environment_id. It returns True if the user successfully navigated to the new environment, otherwise False."

    def _run(self, environment_id: str) -> bool:
        success = navigate_environment(environment_id)
        if success:
            return True

        return False

    def _arun(self, environment_id: str) -> bool:
        return self._run(environment_id)
