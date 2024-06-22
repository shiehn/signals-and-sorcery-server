# rpg_chat.py

import os
import uuid
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from collections import defaultdict  # For managing multiple chat histories

from .tools.environment_tools import DescribeEnvironment
from .tools.item_tools import ListItems, StoreItem
from .tools.navigation_tools import NavigateEnvironment
from .tools.combat_tools import Combat
from .tools.level_up_tools import LevelUp
import logging

logger = logging.getLogger(__name__)


# Define the RPGChat class
class RPGChat:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "As the narrator of this chat-based fantasy RPG, your role is to vividly describe the game world and events, enhancing the player's experience. You try to keep response short usually one or two paragraphs in length.  Use tools to interpret and enrich information about the environment and items without displaying raw data like JSON or technical identifiers to the player. For example, when a player explores a new room, you might describe its eerie ambiance and lurking shadows instead of just listing available exits. Similarly, in combat, focus on creating a dynamic scene rather than only reporting numerical outcomes. Always maintain the narrative's flow and keep technical details in the background, ensuring the story remains immersive and engaging.",
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.tools = [
            DescribeEnvironment(),
            ListItems(),
            StoreItem(),
            NavigateEnvironment(),
            Combat(),
            LevelUp(),
        ]

        # Multi-tenant management with defaultdict
        self.chat_histories = defaultdict(ChatMessageHistory)

    def ask_question(self, user_id, question, api_key):
        if user_id not in self.chat_histories:
            # Initialize new chat history for a new user
            self.chat_histories[user_id] = ChatMessageHistory()

        # Get the specific user's chat history
        user_chat_history = self.chat_histories[user_id]

        # Add the user's question and generate a response
        user_chat_history.add_user_message(question)

        # Initialize ChatOpenAI with the provided API key
        chat = ChatOpenAI(api_key=api_key, model="gpt-4", temperature=0)
        agent = create_openai_tools_agent(chat, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        logger.info("*********************************************************")
        logger.info(f"{user_chat_history.messages[-10:]}")
        logger.info("*********************************************************")

        response = agent_executor.invoke({"messages": user_chat_history.messages[-10:]})
        user_chat_history.add_ai_message(response["output"])

        return response["output"]
