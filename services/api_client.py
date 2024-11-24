import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

# Función para análisis IA
def analyze_text_with_ai(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"text": text, "model": "Meta-Llama-3.1-70B-Instruct-Turbo"}
    try:
        response = requests.post(f"{API_BASE_URL}/analyze", headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return {
                "Coherencia": result.get("coherence", "No evaluado"),
                "Citas y Referencias": result.get("references", "No evaluado"),
                "Formato APA": result.get("apa_compliance", "No evaluado"),
                "Otros Aspectos": result.get("additional_notes", "Ninguno")
            }
        else:
            return {"error": response.json()}
    except requests.RequestException as e:
        return {"error": str(e)}