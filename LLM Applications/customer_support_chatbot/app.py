from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwq"  # Using QWQ for customer support chatbot

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/chat")
def chat_with_ai(user_query: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # Create a structured prompt for a customer support chatbot
    prompt = f"""You are a customer support chatbot. Answer the user's question professionally and concisely.
    User: {user_query}
    Chatbot:"""

    try:
        # Send the query to QWQ
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            headers=headers
        )

        # Log the response for debugging
        print("Ollama Response:", response.text)

        # Ensure valid JSON response
        response_data = response.text.strip()
        try:
            json_response = json.loads(response_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from Ollama: {response_data}")

        # Extract chatbot response
        chatbot_response = json_response.get("response", "I'm sorry, but I couldn't generate a response.")
        return {"response": chatbot_response}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)











