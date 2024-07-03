from langchain_core.tools import BaseTool

from game_engine.api.environment import navigate_environment


class NavigateEnvironment(BaseTool):
    name = "NavigateEnvironment"
    description = "Use this tool to navigate the user through a given door id to a new environment. This tool takes one parameter, a door id. It returns 'success' if the user successfully navigated to the new environment through the door, otherwise a message to be relayed to the user."

    def _run(self, door_id: str) -> str:
        return navigate_environment(door_id)

    def _arun(self, door_id: str) -> str:
        return self._run(door_id)
