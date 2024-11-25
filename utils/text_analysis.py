from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from langdetect import detect
from textblob import TextBlob
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Lista de palabras comunes en español (stopwords)
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

def detect_language(text):
    """
    Detecta el idioma del texto utilizando `langdetect`.
    """
    try:
        return detect(text)
    except Exception:
        return "unknown"

def sentiment_analysis(text):
    """
    Realiza un análisis de sentimiento utilizando `TextBlob`.
    """
    try:
        blob = TextBlob(text)
        return {
            "polarity": blob.sentiment.polarity,  # -1 (negativo) a 1 (positivo)
            "subjectivity": blob.sentiment.subjectivity  # 0 (objetivo) a 1 (subjetivo)
        }
    except Exception:
        return {"polarity": None, "subjectivity": None}

def analyze_text(text):
    """
    Realiza un análisis detallado del texto, incluyendo estadísticas, lenguaje,
    sentimiento, y palabras más comunes.
    """
    try:
        language = detect_language(text)
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(re.findall(r'[.!?]', text))
        
        # Extraer palabras más comunes excluyendo stopwords
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        most_common_words = Counter(filtered_words).most_common(5)

        # Análisis de sentimiento
        sentiment = sentiment_analysis(text)

        return {
            "language": language,
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": sentence_count,
            "most_common_words": most_common_words,
            "sentiment": sentiment,
        }
    except Exception as e:
        raise ValueError(f"Error en el análisis del texto: {e}")

def generate_wordcloud(text):
    """
    Genera una nube de palabras excluyendo palabras comunes (stopwords).
    """
    try:
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        wordcloud_text = " ".join(filtered_words)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wordcloud_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        return plt
    except Exception as e:
        raise ValueError(f"Error al generar la nube de palabras: {e}")