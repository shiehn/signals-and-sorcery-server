# Define custom tools with proper arguments and descriptions
from langchain_core.tools import BaseTool

from game_engine.api.environment import get_environment


# ENVIRONMENT TOOLS


class CurrentEnvironment(BaseTool):
    name = "DescribeEnvironment"
    description = "Get a description of an environment for a provided environment_id"

    def _run(self, environment_id: str):
        return "def"

    def _arun(self, environment_id: str):
        return self._run(environment_id)


class DescribeEnvironment(BaseTool):
    name = "DescribeEnvironment"
    description = "Get a description of an environment for a provided environment_id"

    def _run(self, environment_id: str):
        return get_environment(environment_id)

    def _arun(self, environment_id: str):
        return self._run(environment_id)


# ITEM TOOLS


# STORAGE TOOLS
