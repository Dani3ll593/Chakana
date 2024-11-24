import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v1")
API_KEY = os.getenv("AIML_API_KEY")


def get_model_feedback(text):
    """
    Sends text to the AI/ML API and retrieves feedback.
    """
    if not API_BASE_URL or not API_KEY:
        raise ValueError("API_BASE_URL or API_KEY is not set in the environment.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Construct the payload
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert assistant for research writing analysis. Your task is to evaluate the provided "
                    "text for its academic quality, coherence, and alignment with research objectives. Provide actionable "
                    "feedback in detail, organized as follows:\n"
                    "1. Writing Quality: Grammar, vocabulary, and tone.\n"
                    "2. Coherence: Logical flow and transitions.\n"
                    "3. Relevance: Alignment with research objectives.\n"
                    "4. Recommendations: Specific steps for improvement.\n"
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        "max_tokens": 1000,  # Adjust token limit based on expected feedback size
        "stream": False,  # Set to True for real-time response (optional)
    }

    # Make the API request
    response = requests.post(
        url=f"{API_BASE_URL}/chat/completions",
        headers=headers,
        data=json.dumps(payload),
    )

    # Handle response
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].split("\n")
    else:
        raise Exception(
            f"API error: {response.status_code} - {response.text}"
        )