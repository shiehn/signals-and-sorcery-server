from langchain_core.tools import BaseTool
from game_engine.api.riddles_and_clues import get_clues, solve_riddle, get_riddle


class GetClues(BaseTool):
    name = "GetClues"
    description = "List clues and hints needed to solve the riddle given a environment_id. This tool takes one parameter environment_id. It returns a clues if one is found."

    def _run(self, environment_id: str):
        return get_clues(environment_id)

    def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)


class GetRiddle(BaseTool):
    name = "GetRiddle"
    description = "Get the end of level riddle from an environment_id. This tool takes one parameter environment_id. It returns riddle if it is found."

    def _run(self, environment_id: str):
        return get_riddle(environment_id)

    def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)


class SolveRiddle(BaseTool):
    name = "SolveRiddle"
    description = "Get the end of level riddle from an environment_id. This tool takes one parameter environment_id. It returns riddle if it is found."

    def _run(self, environment_id: str, answer: str):
        return solve_riddle(environment_id, answer)

    def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)
