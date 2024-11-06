from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory

import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Initialize the language model
llm = ChatGoogleGenerativeAI(model=os.environ.get('GOOGLE_MODEL'), api_key=os.environ.get('GOOGLE_API_KEY'))  # type: ignore

# Dictionary to stored chat histories based on => user_id and conversation_id
store = {}

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

#  Allows to store and handle a list of messages as chat history."
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)

    def clear(self) -> None:
        self.messages = []


# If a session exists then store; if not, it creates one with InMemoryHistory and returns it.
def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = InMemoryHistory()
    return store[(user_id, conversation_id)]

# Chain
chain = prompt | llm

# 
with_message_history = RunnableWithMessageHistory(
    chain, # type: ignore
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)

# Chat function for Gradio
def chat(username, user_query):
    # Generate user and conversation IDs based on the username
    user_id = username
    conversation_id = "1"  # Assume single ongoing conversation per user for simplicity

    # Invoke the model with the user's query and retrieve session context
    response = with_message_history.invoke(
        {"question": user_query},
        config={"configurable": {"user_id": user_id, "conversation_id": conversation_id}}
    ).content
    
    return response

user_query_1 = "Hi, my name is Vinod, I would like to know brief 2 line information about AI"
result = chat("Vinod", user_query_1)
print("====== First Response =========")
print(result)

user_query_2 = "What is 1+1?"
result = chat("Vinod", user_query_2)
print("====== Second Response =========")
print(result)

user_query_3 = "Do you remember what is my name?"
result = chat("Vinod", user_query_3)
print("====== Final Response =========")
print(result)

