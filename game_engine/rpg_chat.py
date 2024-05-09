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


open_api_key = os.getenv("OPENAI_API_KEY")


# Define the RPGChat class
class RPGChat:
    def __init__(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an LLM narrating a chat-based fantasy RPG. You use provided tools to interact with the user's environment, embellishing the environment and interactions based on tool outputs.  Internally you use the provided JSON api but you don't display JSON or technical data to the user. Use item_id 's when referring to items and storage. Use environment_id when interacting with the current environment.  Use the ids of the doors array to navigate between environments.",
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.chat = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        tools = [DescribeEnvironment(), ListItems(), StoreItem(), NavigateEnvironment()]

        self.agent = create_openai_tools_agent(self.chat, tools, prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)

        # Multi-tenant management with defaultdict
        self.chat_histories = defaultdict(ChatMessageHistory)

    def ask_question(self, user_id, question):
        if user_id not in self.chat_histories:
            # Initialize new chat history for a new user
            self.chat_histories[user_id] = ChatMessageHistory()

        # Get the specific user's chat history
        user_chat_history = self.chat_histories[user_id]

        # Add the user's question and generate a response
        user_chat_history.add_user_message(question)
        response = self.agent_executor.invoke({"messages": user_chat_history.messages})
        user_chat_history.add_ai_message(response["output"])

        return response["output"]


# Example usage
# if __name__ == "__main__":
#     rpg_chat = RPGChat()
#
#     keep_asking = True
#
#     while keep_asking:
#         user_uuid = uuid.uuid4()  # Generate a unique UUID for the user
#         user_question = input("ADVENTURER: ")
#         if user_question.lower() in ["quit", "exit"]:
#             keep_asking = False
#         else:
#             response = rpg_chat.ask_question(user_uuid, user_question)
#             print(f"BOT: {response}")
