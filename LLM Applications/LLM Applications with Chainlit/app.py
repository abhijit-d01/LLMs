# app.py
import chainlit as cl
from src.llm import ask_order
from src.prompt import system_instruction  # Import the system instruction

@cl.on_chat_start
async def start_chat():
    """
    This function runs at the start of a new chat session.
    It initializes the conversation history with the system prompt.
    """
    # The messages list is now stored in the user session,
    # ensuring it's unique to each chat.
    messages = [
        {"role": "system", "content": system_instruction}
    ]
    cl.user_session.set("messages", messages)
    await cl.Message(content=f"Chat session started!").send()

@cl.on_message
async def main(message: cl.Message):
    """
    This function handles every user message.
    """
    # Retrieve the messages list from the user session
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": message.content})
    
    # Call the LLM with the full message history
    response = ask_order(messages)
    messages.append({"role": "assistant", "content": response})

    # Send the LLM's response back to the user
    await cl.Message(
        content=response,
    ).send()