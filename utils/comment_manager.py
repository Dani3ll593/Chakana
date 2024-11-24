import json
import os
from datetime import datetime

# Ruta de almacenamiento para los comentarios
COMMENTS_FILE = "comments.json"

# Cargar comentarios desde el archivo JSON
def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r") as file:
            return json.load(file)
    return []

# Guardar comentarios en el archivo JSON
def save_comment(selected_text, user, comment):
    comments = load_comments()
    new_comment = {
        "text": selected_text,
        "user": user,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comment": comment,
    }
    comments.append(new_comment)
    with open(COMMENTS_FILE, "w") as file:
        json.dump(comments, file, indent=4)

# Relacionar comentarios con el texto
def get_comments_for_text(selected_text):
    comments = load_comments()
    return [c for c in comments if c["text"] == selected_text]