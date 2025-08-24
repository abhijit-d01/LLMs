from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
import pandas as pd

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "granite3.2"  # Using Granite 3.2 for product recommendations

# Sample Product Database (Can be expanded)
products = [
    {"id": 1, "category": "Electronics", "name": "Wireless Earbuds"},
    {"id": 2, "category": "Electronics", "name": "Smartphone"},
    {"id": 3, "category": "Electronics", "name": "Laptop"},
    {"id": 4, "category": "Fashion", "name": "Leather Jacket"},
    {"id": 5, "category": "Fashion", "name": "Running Shoes"},
    {"id": 6, "category": "Home", "name": "Smart Vacuum Cleaner"},
    {"id": 7, "category": "Home", "name": "Air Purifier"},
]

# Convert to DataFrame for easy filtering
df = pd.DataFrame(products)

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/recommend")
def recommend_products(preferences: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # Generate recommendation prompt
    prompt = f"""You are an AI product recommender. Based on the user's preferences, suggest the best matching products.
    
    User Preferences: {preferences}
    
    Recommended Products:
    """

    try:
        # Send preferences to Granite 3.2 for recommendations
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

        ai_recommendations = json_response.get("response", "No recommendations found.")

        return {"recommendations": ai_recommendations}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Ollama failed: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)








