import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import re

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
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
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
        if results and 'analysis' in results[0]:
            summary_paragraph_1 = results[0]['analysis'].get('summary_paragraph_1', "No se pudo generar el resumen.")
            summary_paragraph_2 = results[0]['analysis'].get('summary_paragraph_2', "No se pudo generar el resumen.")
            summary_paragraph_3 = (
                f"Análisis de sentimiento: {results[0]['analysis']['Análisis de sentimiento']}\n"
                f"Legibilidad: {results[0]['analysis']['Legibilidad']}\n"
                f"Diversidad léxica: {results[0]['analysis']['Diversidad léxica']}"
            )
            return results, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3
        else:
            summary_paragraph_1 = "Error en la generación del análisis."
            summary_paragraph_2 = "Consulta los logs para más detalles."
            summary_paragraph_3 = ""
            return results, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3

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

    def analyze_document(self, text):
        try:
            if not text or len(text.strip()) == 0:
                raise ValueError("El texto proporcionado es inválido o está vacío.")
            analysis_result = self.analyze_text(text)
            text_segments = self.split_into_sections(text)
            academic_quality_results = []
            for segment in text_segments:
                academic_quality_result = self.analyze_academic_quality(segment["content"])
                academic_quality_results.extend(academic_quality_result)
            logging.info(f"Academic Quality Result: {academic_quality_results}")
            if academic_quality_results and 'analysis' in academic_quality_results[0]:
                summary_paragraph_1 = academic_quality_results[0]['analysis'].get('summary_paragraph_1', "No se pudo generar el resumen.")
                summary_paragraph_2 = academic_quality_results[0]['analysis'].get('summary_paragraph_2', "No se pudo generar el resumen.")
                summary_paragraph_3 = (
                    f"Análisis de sentimiento: {analysis_result['Análisis de sentimiento']}\n"
                    f"Legibilidad: {analysis_result['Legibilidad']}\n"
                    f"Diversidad léxica: {analysis_result['Diversidad léxica']}"
                )
                return analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3
            else:
                summary_paragraph_1 = "Error en la generación del análisis."
                summary_paragraph_2 = "Consulta los logs para más detalles."
                summary_paragraph_3 = ""
                return analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3
        except ValueError as e:
            logging.error(f"Error al analizar el texto: {e}")
            raise ValueError(f"Error al analizar el texto: {e}")
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            raise ValueError(f"Error inesperado: {e}")