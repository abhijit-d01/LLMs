import google.generativeai as genai
import os
from dotenv import load_dotenv

from src.prompt import system_instruction

# Load environment variables from the .env file.
load_dotenv()

# Get the API key from the environment.
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Configure the Gemini API with the loaded key.
genai.configure(api_key=api_key)

# Initialize the GenerativeModel.
# We'll use a globally defined model so it can be reused across function calls.
# The 'gemini-1.5-pro' model is a good, powerful choice.
model = genai.GenerativeModel('gemini-1.5-flash')

def ask_order(messages, temperature=0):
    """
    Sends a list of messages to the Gemini API and returns the response.
    Note: Gemini API requires a different message format.
    """
    # Gemini API's system instructions work differently. We'll prepend the
    # system instruction to the first user message.
    
    if messages and messages[0]['role'] == 'system':
        system_instruction_content = messages[0]['content']
        # Remove the system message from the list to avoid duplicate content
        messages = messages[1:]
        
        # Check if there is a first user message to prepend to
        if messages and messages[0]['role'] == 'user':
            messages[0]['content'] = f"{system_instruction_content}\n\n{messages[0]['content']}"

    # Convert the messages to the format required by the Gemini API.
    gemini_messages = []
    for msg in messages:
        # The API roles are 'user' and 'model'.
        role = 'user' if msg['role'] == 'user' else 'model'
        gemini_messages.append({'role': role, 'parts': [{'text': msg['content']}]})

    response = model.generate_content(
        contents=gemini_messages,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature
        )
    )

    # The generated content is accessed via the .text attribute.
    return response.text