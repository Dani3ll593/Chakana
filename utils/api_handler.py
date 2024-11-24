import os
import requests

BASE_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

def analyze_text(text):
    """Enviar texto a la API para análisis."""
    url = f"{BASE_URL}/analyze"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"text": text}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error en la API: {response.status_code} - {response.text}")

def generate_report(sections):
    """Generar un reporte basado en los resultados de análisis."""
    observations = []
    for section, content in sections.items():
        result = analyze_text(content)
        observations.append(f"Sección: {section}\nObservaciones:\n{result.get('suggestions', 'Sin observaciones.')}\n")

    return "\n\n".join(observations)