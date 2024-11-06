from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
# Chain & Memory
from langchain.memory import ConversationSummaryBufferMemory
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
prompt = ChatPromptTemplate.from_template("Tell me about {input}. Previous conversation: {history}")

# Memory
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=2000)

# Completion Method 
def get_completion(usg_msg, memory, verbose):
    runnable_sequence = prompt | llm | StrOutputParser()
    # Retrieve chat history from memory
    chat_history = memory.load_memory_variables({})
    # Run the sequence with both `input` and `history`
    result = runnable_sequence.invoke({
        "input": usg_msg,
        "history": chat_history
    }, verbose = verbose)
    # Update memory with the new conversation
    memory.save_context({"input": usg_msg}, {"output": result})
    return result

# Main Method
if __name__ == "__main__":
    
    user_query_1 = "Hi, my name is Vinod"
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

    
    
    