import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.aimlapi.com/v1")
API_KEY = os.getenv("API_KEY")


def get_model_feedback(text):
    """
    Sends text to the API and retrieves AI feedback with precise, actionable insights.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Detailed system prompt for the AI
    system_prompt = (
        "You are an advanced AI model specializing in research writing analysis. Your task is to provide "
        "detailed and actionable feedback on the user's research text based on the following criteria:\n"
        "1. Writing Quality:\n"
        "   - Grammar, spelling, and punctuation.\n"
        "   - Clarity and conciseness of the language.\n"
        "   - Appropriate use of academic tone and vocabulary.\n"
        "2. Coherence and Structure:\n"
        "   - Logical flow of ideas and proper organization.\n"
        "   - Transitions between sentences and paragraphs.\n"
        "   - Alignment of the text with the research objectives and theoretical framework.\n"
        "3. Specific Feedback:\n"
        "   - Highlight specific sentences or sections that require improvement.\n"
        "   - Suggest alternative phrasing or restructured sentences where needed.\n"
        "   - Point out inconsistencies or gaps in logic, and recommend ways to address them.\n"
        "4. Recommendations:\n"
        "   - Provide prioritized, step-by-step suggestions to improve the quality and coherence of the text.\n"
        "   - Offer guidance on enhancing alignment with research objectives.\n"
    )

    # User content is the text to be analyzed
    user_prompt = (
        "Analyze the following research text based on the above criteria and provide detailed feedback. "
        "Ensure each comment is precise, actionable, and linked to a specific issue in the text:\n"
        f"{text}"
    )

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000  # Increased token limit for detailed feedback
    }

    response = requests.post(f"{API_BASE_URL}/chat/completions", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].split("\n")
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")