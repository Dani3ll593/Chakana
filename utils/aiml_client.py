import requests
import re

class AIMLClient:
    def __init__(self, api_url, api_key):
        """
        Inicializa el cliente AIML con la URL base y la clave de la API.
        """
        self.api_url = api_url
        self.api_key = api_key

    def _make_request(self, endpoint, payload):
        """
        Realiza una solicitud POST a la API y maneja errores.
        """
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Verifica si el código de respuesta indica un error
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al comunicarse con la API: {e}")
        except Exception as e:
            raise ValueError(f"Error desconocido: {e}")

    def analyze_text(self, text):
        """
        Analiza un texto en busca de coherencia y redacción.
        """
        endpoint = f"{self.api_url}/analyze"
        return self._make_request(endpoint, {"text": text})

    def analyze_sentiment(self, text):
        """
        Analiza el sentimiento de un texto.
        """
        endpoint = f"{self.api_url}/sentiment"
        return self._make_request(endpoint, {"text": text})

    def analyze_academic_quality(self, text):
        """
        Analiza la calidad académica de un texto dividido en secciones.
        """
        sections = self.split_into_sections(text)
        results = []
        for section in sections:
            section_text = section["content"].strip()
            if section_text:  # Evitar secciones vacías
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
        """
        Divide el texto en secciones basándose en líneas en mayúsculas.
        """
        sections = []
        current_section = {"title": None, "content": ""}
        lines = text.splitlines()

        for i, line in enumerate(lines):
            line = line.strip()
            if re.match(r"^[A-Z\s]+$", line):  # Detectar líneas en mayúsculas como títulos
                if current_section["title"]:  # Guardar la sección previa
                    sections.append(current_section)
                current_section = {"title": line, "content": ""}
            elif line:  # Añadir contenido a la sección actual
                current_section["content"] += line + " "

        # Agregar la última sección si tiene título
        if current_section["title"]:
            sections.append(current_section)

        return sections