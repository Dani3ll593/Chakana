import requests
import re
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class AIMLClient:
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
            logging.info(f"API Response: {response.json()}")  # Agregar log para la respuesta de la API
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error HTTP al comunicarse con la API: {e.response.status_code} {e.response.reason}")
            raise ValueError(f"Error HTTP al comunicarse con la API: {e.response.status_code} {e.response.reason}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al comunicarse con la API: {e}")
            raise ValueError(f"Error al comunicarse con la API: {e}")

    def analyze_text(self, text):
        endpoint = f"{self.api_url}/analyze"
        payload = {
            "text": text,
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Asegurar el uso del modelo especificado
            "max_tokens": 200,  # Permitir hasta 200 tokens
            "temperature": 0.7,  # Asegurar que la temperatura sea 0.7
            "top_p": 0.9,  # Ajustar top_p para mayor creatividad
            "frequency_penalty": 0.5,  # Penalizar la frecuencia para evitar repeticiones
            "presence_penalty": 0.6,  # Penalizar la presencia para fomentar la diversidad
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
        return self._make_request(endpoint, payload)

    def analyze_sentiment(self, text):
        endpoint = f"{self.api_url}/sentiment"
        payload = {
            "text": text,
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Asegurar el uso del modelo especificado
            "max_tokens": 200  # Permitir hasta 200 tokens
        }
        return self._make_request(endpoint, payload)

    def analyze_academic_quality(self, text):
        sections = self.split_into_sections(text)
        results = []
        for section in sections:
            section_text = section["content"].strip()
            if section_text:
                try:
                    analysis_result = self.analyze_text(section_text)
                    results.append({
                        "section_title": section["title"],
                        "analysis": analysis_result
                    })
                except ValueError as e:
                    results.append({
                        "section_title": section["title"],
                        "error": str(e)
                    })
        return results

    def split_into_sections(self, text):
        sections = []
        current_section = {"title": None, "content": ""}
        lines = text.splitlines()

        for line in lines:
            line = line.strip()
            if re.match(r"^[A-Z\s]+$", line):
                if current_section["title"]:
                    sections.append(current_section)
                current_section = {"title": line, "content": ""}
            elif line:
                current_section["content"] += line + " "

        if current_section["title"]:
            sections.append(current_section)

        return sections