import os
import requests
from utilities.config import get_api_config

def analyze_text(text):
    api_url, api_key = get_api_config()
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "input": text,
        "parameters": {
            "analysis_type": "academic_review"
        }
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}