import requests
import re

class AIMLClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def analyze_text(self, text):
        endpoint = f"{self.api_url}/analyze"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"text": text}
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al comunicarse con la API: {e}")

    def analyze_sentiment(self, text):
        endpoint = f"{self.api_url}/sentiment"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"text": text}
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al analizar el sentimiento: {e}")

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
        for i, line in enumerate(lines):
            if re.match(r"^\s*[A-Z\s]{3,}\s*$", line):
                if current_section["title"]:
                    sections.append(current_section)
                current_section = {"title": line.strip(), "content": ""}
            else:
                current_section["content"] += line.strip() + " "
        if current_section["title"]:
            sections.append(current_section)
        return sections