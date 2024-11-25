from wordcloud import WordCloud
import matplotlib.pyplot as plt

def analyze_text(text):
    word_count = len(text.split())
    char_count = len(text)
    return {"word_count": word_count, "char_count": char_count}

def summarize_text(client, text):
    return client.request_summary(text)

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return plt