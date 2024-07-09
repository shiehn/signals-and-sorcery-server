import logging
import random

from game_engine.api.event_publisher import EventPublisher
from byo_network_hub.models import (
    GameMap,
    GameState,
    GameElementLookup,
)

logger = logging.getLogger(__name__)


def get_clues(environment_id: str):
    # Retrieve user ID based on the environment ID
    user_id = GameElementLookup.objects.get(element_id=environment_id).user_id

    # Retrieve game state for the user
    game_state = GameState.objects.filter(user_id=user_id).first()
    map_id = game_state.map_id

    # Retrieve the game map graph
    game_map = GameMap.objects.get(id=map_id).map_graph

    # Search for the node by environment_id
    for node in game_map["nodes"]:
        if node["id"] == environment_id:
            # Check if the riddle and clues exist
            if "riddle" in node["game_info"] and "clues" in node["game_info"]["riddle"]:
                clues = node["game_info"]["riddle"]["clues"]
                if clues:
                    return clues[0]  # Return the first clue

    # Default return if no clues found
    return "You have not been able to find any clues, or hints for the riddle."


def get_riddle(environment_id: str):
    user_id = GameElementLookup.objects.get(element_id=environment_id).user_id
    game_state = GameState.objects.filter(user_id=user_id).first()
    map_id = game_state.map_id
    game_map = GameMap.objects.get(id=map_id).map_graph

    for node in game_map["nodes"]:
        if node["id"] == environment_id:
            if (
                "riddle" in node["game_info"]
                and "password" in node["game_info"]["riddle"]
            ):
                riddle_info = node["game_info"]["riddle"]
                options = [riddle_info["password"]["correct"]] + riddle_info[
                    "password"
                ]["incorrect"]
                random.shuffle(
                    options
                )  # Shuffle the options to randomize their order each time
                question = f"To proceed you must select the correct answer. The options are: {', '.join(options)}"
                return question
    return "No riddle is available for this environment."


def solve_riddle(environment_id: str, answer: str):
    user_id = GameElementLookup.objects.get(element_id=environment_id).user_id
    game_state = GameState.objects.filter(user_id=user_id).first()
    map_id = game_state.map_id
    game_map = GameMap.objects.get(id=map_id).map_graph

    # Search for the node by environment_id
    for node in game_map["nodes"]:
        if node["id"] == environment_id:
            # Check if riddle and correct answer exist
            if (
                "riddle" in node["game_info"]
                and "password" in node["game_info"]["riddle"]
            ):
                correct_answer = node["game_info"]["riddle"]["password"]["correct"]
                if answer == correct_answer:
                    return "Riddle solved correctly!"
                else:
                    return "Wrong answer. Try again."

    # Default return if no matching node found
    return "No riddle found for this environment."
