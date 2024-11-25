import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from langdetect import detect
from textblob import TextBlob
from nltk.tokenize import word_tokenize

# Inicializar recursos de NLTK
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)  # Añadir esta línea
except Exception as e:
    raise RuntimeError(f"Error al inicializar recursos NLTK: {e}")

# Stopwords comunes en español
STOPWORDS = {
    "y", "para", "que", "de", "la", "el", "en", "es", "a", "los", "se", "del", "las", "por",
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
    "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras",
    ".", ",", "(", ")", ":", ";", "!", "?", "-", "_", "[", "]", "{", "}", "\"", "'"
}

def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "unknown"

def sentiment_analysis(text):
    try:
        blob = TextBlob(text)
        return {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }
    except Exception:
        return {"polarity": None, "subjectivity": None}

def analyze_text(text):
    try:
        language = detect_language(text)
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(re.findall(r'[.!?]', text))
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        most_common_words = Counter(filtered_words).most_common(5)
        sentiment = sentiment_analysis(text)
        
        # Análisis de legibilidad
        syllable_count = sum([len(re.findall(r'[aeiouáéíóúü]', word)) for word in words])
        avg_sentence_length = word_count / sentence_count if sentence_count else 0
        avg_syllables_per_word = syllable_count / word_count if word_count else 0
        readability_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word

        # Análisis de diversidad léxica
        unique_words = set(filtered_words)
        lexical_diversity = len(unique_words) / word_count if word_count else 0

        return {
            "Idioma": language,
            "Número de palabras": word_count,
            "Número de caracteres": char_count,
            "Número de oraciones": sentence_count,
            "Palabras más comunes": [{"palabra": word, "frecuencia": freq} for word, freq in most_common_words],
            "Análisis de sentimiento": {
                "Polaridad": sentiment["polarity"],
                "Subjetividad": sentiment["subjectivity"]
            },
            "Legibilidad": readability_score,
            "Diversidad léxica": lexical_diversity
        }
    except Exception as e:
        raise ValueError(f"Error en el análisis del texto: {e}")

def generate_wordcloud(text):
    try:
        if not text:
            raise ValueError("El texto proporcionado está vacío.")
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        if not filtered_words:
            raise ValueError("No se encontraron palabras válidas para generar la nube de palabras.")
        wordcloud_text = " ".join(filtered_words)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wordcloud_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        return plt
    except Exception as e:
        raise ValueError(f"Error al generar la nube de palabras: {e}")