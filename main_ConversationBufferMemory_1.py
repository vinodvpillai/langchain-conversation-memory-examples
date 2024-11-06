from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
# Chain & Memory
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.chat import ChatPromptTemplate
# Env variable
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Loading the environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# LLM
llm = ChatGoogleGenerativeAI(model=os.environ.get('GOOGLE_MODEL'), api_key=os.environ.get('GOOGLE_API_KEY'))  # type: ignore

# Prompt
prompt = ChatPromptTemplate.from_template("Tell me about {text}. Previous conversation: {chat_history}")

# Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Completion Method 
def get_completion(usg_msg, memory, verbose):
    runnable_sequence = prompt | llm | StrOutputParser()
    # Retrieve chat history from memory
    chat_history = memory.load_memory_variables({}).get("chat_history", "")
    # Run the sequence with both `text` and `chat_history`
    result = runnable_sequence.invoke({
        "text": usg_msg,
        "chat_history": chat_history
    }, verbose = verbose)
    # Update memory with the new conversation
    memory.save_context({"text": usg_msg}, {"output": result})
    return result

# Main Method
if __name__ == "__main__":
    
    user_query_1 = "Hi, my name is Vinod, I would like to know brief 2 line information about AI"
    response = get_completion(user_query_1, memory, False)
    print("====== First Response =========")
    print(response)
    
    user_query_2 = "What is 1+1?"
    response = get_completion(user_query_2, memory, True)
    print("====== Second Response =========")
    print(response)
    
    user_query_3 = "Do you remember what is my name?"
    response = get_completion(user_query_3, memory, False)
    print("====== Final Response =========")
    print(response)

    
    
    