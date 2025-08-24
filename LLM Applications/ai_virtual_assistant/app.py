from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
import datetime

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"  # Using LLaMA 2 for AI Virtual Assistant

# Store scheduled tasks
scheduled_tasks = []

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/chat")
def chat_with_ai(user_query: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    prompt = f"""You are an AI-powered virtual assistant that helps with task scheduling and answering queries.
    If the user asks to schedule a task, extract the task details and save it.
    User: {user_query}
    Assistant:"""

    try:
        # Send the query to LLaMA 2
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            headers=headers
        )

        print("Ollama Response:", response.text)

        # Ensure valid JSON response
        response_data = response.text.strip()
        try:
            json_response = json.loads(response_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from Ollama: {response_data}")

        chatbot_response = json_response.get("response", "I'm sorry, but I couldn't generate a response.")
        
        # Check if the user is scheduling a task
        if "schedule" in user_query.lower() or "remind" in user_query.lower():
            task = {"task": user_query, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            scheduled_tasks.append(task)
            chatbot_response += f"\nTask Scheduled: {user_query}"

        return {"response": chatbot_response, "tasks": scheduled_tasks}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)






