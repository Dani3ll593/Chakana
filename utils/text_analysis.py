from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def analyze_text(text):
    """
    Realiza un análisis básico del texto, incluyendo estadísticas de palabras y caracteres.
    """
    try:
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(re.findall(r'[.!?]', text))
        
        # Extraer las palabras más comunes
        words = re.findall(r'\b\w+\b', text.lower())
        most_common_words = Counter(words).most_common(5)
        
        return {
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": sentence_count,
            "most_common_words": most_common_words
        }
    except Exception as e:
        raise ValueError(f"Error en el análisis básico del texto: {e}")

# Lista de stopwords comunes en español
STOPWORDS = {
    "y", "que", "de", "la", "el", "en", "es", "a", "los", "se", "del", "las", "por", 
    "un", "con", "no", "una", "su", "al", "lo", "como", "más", "pero", "sus", "le", 
    "ya", "o", "fue", "ha", "sí", "porque", "esta", "son", "entre", "cuando", "muy", 
    "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien", "desde", 
    "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", 
    "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", 
    "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", 
    "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", 
    "nosotros", "mi", "mis", "tus", "te", "ti", "tu", "sí", "mismo", "él", "sólo", 
    "ellas", "hay", "tú", "vosotros", "vosotras", "os", "míos", "mías", "tuyo", 
    "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", 
    "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras"
}

def preprocess_text(text):
    """
    Limpia el texto eliminando palabras comunes (stopwords) y caracteres no deseados.
    """
    words = re.findall(r'\b\w+\b', text.lower())  # Extraer palabras ignorando mayúsculas/minúsculas
    filtered_words = [word for word in words if word not in STOPWORDS]
    return " ".join(filtered_words)

def generate_wordcloud(text):
    """
    Genera una nube de palabras excluyendo palabras comunes (stopwords).
    """
    try:
        # Preprocesar el texto para eliminar stopwords
        cleaned_text = preprocess_text(text)

        # Crear la nube de palabras
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(cleaned_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        return plt
    except Exception as e:
        raise ValueError(f"Error al generar la nube de palabras: {e}")