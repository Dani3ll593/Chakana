import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class AIMLClient2:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def _make_request(self, endpoint, payload):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            response = self.session.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"API Response: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error HTTP al comunicarse con la API: {e.response.status_code} {e.response.text}")
            raise ValueError(f"Error HTTP al comunicarse con la API: {e.response.status_code} {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al comunicarse con la API: {e}")
            raise ValueError(f"Error al comunicarse con la API: {e}")

    def analyze_text(self, text):
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("El texto proporcionado es inválido o está vacío.")
        endpoint = f"{self.api_url}/analyze"
        payload = {
            "text": text,
            "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.6,
            "prompt": (
                "Por favor, realiza una revisión de la calidad académica del siguiente texto. "
                "Evalúa los siguientes aspectos: "
                "1. Claridad y coherencia del mensaje. "
                "2. Uso de lenguaje académico y apropiado para la audiencia objetivo. "
                "3. Uso de fuentes y citas confiables. "
                "4. Organización lógica y estructuración del contenido. "
                "5. Contribución significativa al campo académico o tema en cuestión."
            )
        }
        logging.info(f"Enviando payload a {endpoint}: {payload}")
        return self._make_request(endpoint, payload)