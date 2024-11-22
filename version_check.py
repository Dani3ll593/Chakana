from dotenv import load_dotenv
import os
load_dotenv("E:/HACKATONS/LLAMA/CHAKANA/Python/.env")  # Carga las variables desde el archivo .env
llama_api_key = os.getenv("LLAMA_API_KEY")  # Obtiene la clave de la API