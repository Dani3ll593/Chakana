# Identificar posición del texto seleccionado
def get_text_indices(full_text, selected_text):
    start_index = full_text.find(selected_text)
    if start_index == -1:
        return None
    end_index = start_index + len(selected_text)
    return {"start": start_index, "end": end_index}
