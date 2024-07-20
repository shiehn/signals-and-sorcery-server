# rpg_chat_service.py

from .singleton import Singleton
from .rpg_chat import RPGChat

import logging

logger = logging.getLogger(__name__)


class RPGChatService(Singleton):
    def __init__(self):
        if not hasattr(self, "initialized"):  # Ensure initialization is done only once
            self.rpg_chat = RPGChat()  # Your RPG chat class
            self.initialized = True

    def track_action_outcome(self, user_id, action, outcome):
        logger.info(f"ACTION: {action}, OUTCOME: {outcome}")
        return self.rpg_chat.add_action_outcome(user_id, action, outcome)

    def ask_question(self, user_id, question, api_key, game_setting=None):
        logger.info(
            f"User {user_id} asked: {question}, with game_setting={game_setting}"
        )
        return self.rpg_chat.ask_question(user_id, question, api_key, game_setting)

    def clear_chat_history(self, user_id):
        # Clear existing chat history if any
        self.rpg_chat.clear_chat_history(user_id)
        logger.info(f"New game started for User {user_id}")
