import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v1")
API_KEY = os.getenv("AIML_API_KEY")

def get_model_feedback(text):
    """
    Sends text to the API and retrieves AI feedback.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are an assistant for research writing analysis."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(f"{API_BASE_URL}/chat/completions", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].split("\n")
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")