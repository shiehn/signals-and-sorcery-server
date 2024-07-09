# rpg_chat.py

import os
import uuid
import re
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from collections import defaultdict  # For managing multiple chat histories

from .tools.environment_tools import DescribeEnvironment
from .tools.item_tools import ListItems, StoreItem
from .tools.navigation_tools import NavigateEnvironment
from .tools.combat_tools import Combat
from .tools.level_up_tools import LevelUp
from .tools.riddle_tools import GetClues, GetRiddle, SolveRiddle
import logging

logger = logging.getLogger(__name__)


# Define the RPGChat class
class RPGChat:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "As the narrator of this LLM based fantasy RPG, your role is to describe the game world and events. You try to keep your response short usually one to three sentences in length. Use tools to save and retrieve state details about the environment and items without displaying raw data like JSON or technical identifiers to the player. For example, when a player explores a new room, you might describe its eerie ambiance and lurking shadows instead of just listing available exits. Similarly, in combat, focus on creating a dynamic scene rather than only reporting numerical outcomes. Always maintain the narrative's flow and keep technical details in the background, ensuring the story remains immersive and engaging.",
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
            GetClues(),
            GetRiddle(),
            SolveRiddle(),
        ]

        # Multi-tenant management with defaultdict
        self.chat_histories = defaultdict(ChatMessageHistory)

    def ask_question(self, user_id, question, api_key):
        def estimate_tokens(text):
            return len(text) // 4  # Approximation: 1 token ~= 4 characters

        def extract_context(message):
            pattern = re.compile(
                r"user_id=[^ ]+ environment_id=[^ ]+ doors=\[[^\]]*\] environment_items=\[[^\]]*\] inventory_items=\[[^\]]*\]"
            )
            match = pattern.search(message)
            return match.group(0) if match else ""

        if user_id not in self.chat_histories:
            # Initialize new chat history for a new user
            self.chat_histories[user_id] = ChatMessageHistory()

        # Get the specific user's chat history
        user_chat_history = self.chat_histories[user_id]

        # Extract the context from the latest question
        latest_context = extract_context(question)
        escaped_latest_context = re.escape(latest_context)
        clean_question = re.sub(escaped_latest_context, "", question).strip()

        # Add the user's clean question to the chat history
        user_chat_history.add_user_message(clean_question)

        # Initialize ChatOpenAI with the provided API key
        # chat = ChatOpenAI(api_key=api_key, model="gpt-4", temperature=0)
        chat = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo-0125", temperature=0)
        agent = create_openai_tools_agent(chat, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        # Calculate the total token length, including the latest question
        total_tokens = estimate_tokens(question)

        # Process the message history in reverse to find the latest context and trim if needed
        trimmed_messages = []
        for message in reversed(user_chat_history.messages):
            content = message.content
            # Remove any previous context from the message content
            content = re.sub(escaped_latest_context, "", content).strip()
            message_tokens = estimate_tokens(content)

            if total_tokens + message_tokens <= 8000:
                trimmed_messages.append(message)
                total_tokens += message_tokens
            else:
                break

        # Reverse to maintain the original order
        trimmed_messages.reverse()

        # Include the latest context in the latest question
        latest_question_with_context = clean_question + " " + latest_context
        trimmed_messages.append(HumanMessage(content=latest_question_with_context))

        logger.info("******************TEN ITEM HISTORY START************************")
        logger.info(f"{trimmed_messages[-10:]}")
        logger.info("******************TEN ITEM HISTORY END  ************************")

        response = agent_executor.invoke({"messages": trimmed_messages})
        user_chat_history.add_ai_message(response["output"])

        return response["output"]
