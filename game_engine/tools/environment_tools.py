# Define custom tools with proper arguments and descriptions
from langchain_core.tools import BaseTool

from game_engine.api.environment import get_environment
from byo_network_hub.models import GameElementLookup


# ENVIRONMENT TOOLS


class DescribeEnvironment(BaseTool):
    name = "DescribeEnvironment"
    description = "Get a description of an environment. This tool takes one parameter which is environment_id."

    def _run(self, environment_id: str):
        element_lookup = GameElementLookup.objects.get(element_id=environment_id)

        if element_lookup is None:
            return "Unable to determine the user's id from the element_lookup"

        user_id = element_lookup.user_id

        if user_id is None:
            return "Unable to determine the user's id"

        return get_environment(environment_id, user_id)

    def _arun(self, environment_id: str):
        return self._run(environment_id)
