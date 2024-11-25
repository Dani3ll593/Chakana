import requests

class AIMLClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def request_summary(self, text):
        response = requests.post(
            f"{self.api_url}/summarize",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"text": text}
        )
        if response.status_code == 200:
            return response.json().get("summary", "No se pudo generar el resumen.")
        else:
            raise ValueError(f"Error en la API: {response.status_code}, {response.text}")