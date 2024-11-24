# Identificar todas las posiciones del texto seleccionado
def get_text_indices(full_text, selected_text):
    indices = []
    start = 0
    while start < len(full_text):
        start = full_text.find(selected_text, start)
        if start == -1:
            break
        indices.append({"start": start, "end": start + len(selected_text)})
        start += len(selected_text)
    return indices