# Conversation Memory Management Programs

This repository contains a collection of Python programs demonstrating various methods for managing conversation memory using LangChain's tools. Each script is designed to showcase different types of memory implementations and how they affect conversational models.

## Overview

These scripts are part of a set designed to handle memory in conversational AI, utilizing LangChain and OpenAI integrations to manage different styles of conversation memory. Each implementation is tailored to a specific use case for developers building applications that require persistent context in user interactions.

## File Descriptions

### 1. `main_ConversationBufferMemory_1.py`

**Description**: Demonstrates how to use `ConversationBufferMemory` to store and recall the entire conversation history in memory. This implementation is suitable for applications that need to access complete conversation records.

**Key Features**:
- Simple and efficient memory buffer.
- Maintains all user and AI interactions.
- Ideal for chatbots that need to reference the entire conversation context.

### 2. `main_ConversationBufferWindowMemory_2.py`

**Description**: Uses `ConversationBufferWindowMemory`, which retains a sliding window of the most recent interactions in the conversation. This approach is useful for applications that need a limited context to avoid overloading memory.

**Key Features**:
- Sliding window of recent interactions.
- Customizable window size to control context length.
- Useful for chatbots that need to keep conversations concise.

### 3. `main_ConversationTokenBufferMemory_3.py`

**Description**: Implements `ConversationTokenBufferMemory`, which stores conversation history up to a specified token limit. This ensures the memory does not exceed a certain number of tokens, making it suitable for applications where token usage must be optimized.

**Key Features**:
- Token-based memory limitation.
- Configurable token count to manage API cost and memory usage.
- Ensures conversations remain within practical size limits.

### 4. `main_ConversationSummaryMemory_4.py`

**Description**: Showcases `ConversationSummaryMemory`, which condenses past interactions into summaries as the conversation progresses. This is ideal for long-term conversations where retaining detailed history is impractical.

**Key Features**:
- Automatic summarization of past conversations.
- Reduces memory load by maintaining a compact context.
- Suitable for applications requiring concise memory with extensive history.

### 5. `main_RunnableWithMessageHistory_5.py`

**Description**: Demonstrates how to manage conversation history using `RunnableWithMessageHistory`. This method enables structured handling of previous messages, allowing more complex memory strategies within conversation chains.

**Key Features**:
- Integrated message handling with advanced customization.
- Allows for branching and merging of memory contexts.
- Flexible for various use cases, such as context-dependent question answering.

## Requirements

Ensure the following dependencies are installed:

- Python 3.10+
- LangChain (`pip install langchain`)
- Google Generative AI(`langchain-google-genai`)
- Additional libraries as needed (refer to individual script headers for more details)

## Usage

Each script can be run independently. To execute a script, use the following command:

```bash
python main_ConversationBufferMemory_1.py
```

Replace `main_ConversationBufferMemory_1.py` with the desired script name to run other memory management examples.

## License

This project is licensed under the MIT License.