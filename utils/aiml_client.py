import requests

class AIMLClient:
    def __init__(self, api_url, api_key):
        """
        Inicializa el cliente AIML con la URL base y la clave de la API.
        """
        self.api_url = api_url
        self.api_key = api_key

    def analyze_text(self, text):
        """
        Envía el texto para su análisis a la API de IA y retorna los resultados.
        """
        endpoint = f"{self.api_url}/analyze"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"text": text}
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Lanza un error si el código de estado no es 200
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al comunicarse con la API: {e}")
        except Exception as e:
            raise ValueError(f"Error desconocido: {e}")