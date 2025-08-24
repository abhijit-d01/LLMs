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
MODEL_NAME = "medllama2"  # Using MedLLaMA 2 for symptom analysis

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/analyze_symptoms")
def analyze_symptoms(symptoms: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    prompt = f"""You are a medical AI assistant trained to analyze symptoms. 
    Based on the provided symptoms, give possible explanations and general advice. 
    Do not provide a diagnosis or replace a doctor's consultation.
    
    User Symptoms: {symptoms}
    
    Medical AI:"""

    try:
        # Send the symptoms to MedLLaMA 2
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

        ai_response = json_response.get("response", "I'm sorry, but I couldn't generate a response.")
        return {"response": ai_response}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)









