# Análisis avanzado del texto
def analyze_document(response):
    if "error" in response:
        return {"message": "Error en el análisis de texto", "details": response["error"]}

    result = response.get("analysis", {})
    formatted_analysis = {
        "Coherencia": result.get("coherence"),
        "Normas APA": result.get("apa_format"),
        "Normas Vancouver": result.get("vancouver_format"),
        "Normas Chicago": result.get("chicago_format"),
        "Lógica y flujo": result.get("logical_flow"),
    }
    return formatted_analysis