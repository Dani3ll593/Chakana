import os
from dotenv import load_dotenv

load_dotenv()

def get_api_config():
    return os.getenv("AIML_BASE_URL"), os.getenv("AIML_API_KEY")