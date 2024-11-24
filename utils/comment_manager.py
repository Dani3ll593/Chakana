import json
import os
from datetime import datetime

COMMENTS_FILE = "comments.json"

# Cargar comentarios desde el archivo JSON
def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r") as file:
            return json.load(file)
    return []

# Guardar un comentario
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