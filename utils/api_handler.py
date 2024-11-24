import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

# Debugging environment variables
if not API_BASE_URL or not API_KEY:
    print("DEBUG: API_BASE_URL or API_KEY is missing.")
    raise ValueError("API_BASE_URL or API_KEY is missing. Ensure .env is set up correctly.")

def get_model_feedback(text, temperature=0.7, max_tokens=1000, writing_style=None):
    """
    Sends text to the AI/ML API and retrieves AI feedback in paragraph form.
    
    Parameters:
        - text (str): The research text to analyze.
        - temperature (float): Controls the randomness of the output.
        - max_tokens (int): Maximum tokens in the AI's response.
        - writing_style (str): The writing style for evaluation (APA, Chicago, Vancouver, etc.).
        
    Returns:
        - feedback (str): A detailed feedback paragraph from the AI.
    """
    # Define default criteria
    criteria = [
        "writing quality (grammar, clarity, and conciseness)",
        "coherence and logical structure",
        "alignment with research objectives and theoretical framework",
    ]

    # Add style-specific criteria
    if writing_style and writing_style != "None":
        criteria.append(f"adherence to the {writing_style} writing style")

    # Construct the system prompt
    criteria_str = ", ".join(criteria)
    system_prompt = (
        "You are an advanced AI assistant specializing in research and formatting analysis. Your task is to provide "
        "clear, detailed, and constructive feedback on research text. Focus on the following aspects: "
        f"{criteria_str}. "
        "Ensure the feedback is organized into a single cohesive paragraph with specific examples or suggestions."
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    # Return the feedback as a single paragraph
    return response.json()["choices"][0]["message"]["content"].strip()