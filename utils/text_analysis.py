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
    try:
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        wordcloud_text = " ".join(filtered_words)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wordcloud_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        return plt
    except Exception as e:
        raise ValueError(f"Error al generar la nube de palabras: {e}")