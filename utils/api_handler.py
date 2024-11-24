import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env
load_dotenv()

# Load the API key and base URL from environment variables
API_BASE_URL = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v1")
API_KEY = os.getenv("AIML_API_KEY")

def get_model_feedback(text):
    """
    Sends text to the AI/ML API and retrieves AI feedback using the OpenAI-compatible API structure.
    """
    if not API_BASE_URL or not API_KEY:
        raise ValueError("API_BASE_URL or API_KEY is missing. Ensure .env is set up correctly.")

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Payload for the API request
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are an advanced AI assistant for research analysis."},
            {"role": "user", "content": text},
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    # Make the API request
    try:
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Request error occurred: {req_err}")