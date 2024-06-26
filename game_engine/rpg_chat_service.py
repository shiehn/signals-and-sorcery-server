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

    def ask_question(self, user_id, question, api_key):
        logger.info(f"User {user_id} asked: {question}")
        return self.rpg_chat.ask_question(user_id, question, api_key)
