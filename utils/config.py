import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def get_api_config():
    """
    Obtiene las variables de configuración necesarias para la API.
    """
    base_url = os.getenv("AIML_BASE_URL")
    api_key = os.getenv("AIML_API_KEY")
    
    if not base_url or not api_key:
        raise ValueError("API configuration variables are missing in the .env file.")
    
    return base_url, api_key