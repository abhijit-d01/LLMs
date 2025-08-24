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
MODEL_NAME = "codellama"  # Using CodeLlama for code generation & debugging

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/generate_code")
def generate_code(prompt: str = Form(...), mode: str = Form(...)):
    headers = {"Content-Type": "application/json"}
    
    # Define prompts based on mode (generate or debug)
    if mode == "generate":
        full_prompt = f"Write a clean, well-documented {prompt} code snippet."
    elif mode == "debug":
        full_prompt = f"Debug and fix the following code:\n{prompt}"
    else:
        raise HTTPException(status_code=400, detail="Invalid mode selected.")

    try:
        # Send the request to Ollama
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False},
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

        # Extract the generated or debugged code
        generated_code = json_response.get("response", "No valid response received.")
        return {"code": generated_code}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
