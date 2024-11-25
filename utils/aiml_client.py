import requests
import re

class AIMLClient:
    def __init__(self, api_url, api_key):
        """
        Inicializa el cliente AIML con la URL base y la clave de la API.
        """
        self.api_url = api_url
        self.api_key = api_key

    def analyze_text(self, text):
        """
        Envía el texto para análisis a la API. Ajustamos el payload y validamos la respuesta.
        """
        endpoint = f"{self.api_url}/analyze"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"text": text}

        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Lanza un error si el código de estado no es 200
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al comunicarse con la API: {e}")
        except Exception as e:
            raise ValueError(f"Error desconocido: {e}")

    def split_into_sections(self, text):
        """
        Divide el texto en secciones basándose en títulos y subtítulos.
        Considera líneas en mayúsculas como títulos y combina subtítulos si están inmediatamente debajo.
        """
        sections = []
        current_section = {"title": None, "content": ""}

        lines = text.splitlines()
        for i, line in enumerate(lines):
            if re.match(r"^\s*[A-Z\s]{3,}\s*$", line):  # Detectar títulos (mayúsculas, mínimo 3 caracteres)
                if current_section["title"]:  # Guardar la sección previa antes de iniciar una nueva
                    sections.append(current_section)
                current_section = {"title": line.strip(), "content": ""}
            elif re.match(r"^\s*[A-Za-z\s,]+\s*$", line) and i > 0 and re.match(r"^\s*[A-Z\s]{3,}\s*$", lines[i - 1]):
                # Si es un subtítulo, agruparlo con el título previo
                current_section["title"] += f" - {line.strip()}"
            else:
                # Agregar contenido a la sección actual
                current_section["content"] += line.strip() + " "

        # Agregar la última sección al final
        if current_section["title"]:
            sections.append(current_section)

        return sections

    def analyze_academic_quality(self, text):
        """
        Analiza la calidad académica de cada sección del texto y retorna los resultados.
        """
        sections = self.split_into_sections(text)
        results = []

        for section in sections:
            section_text = section["content"].strip()
            if section_text:  # Evitar enviar secciones vacías
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