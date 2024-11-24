import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

# Función para analizar texto usando la API de Meta-Llama
def analyze_text_with_ai(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model": "Meta-Llama-3.1-70B-Instruct-Turbo"
    }

    response = requests.post(f"{API_BASE_URL}/analyze", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}