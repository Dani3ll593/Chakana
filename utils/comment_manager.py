class CommentManager:
    def __init__(self):
        # Diccionario que almacena comentarios, clave = sección, valor = lista de comentarios
        self.comments = {}
        self.active_section = None

    def set_active_section(self, section):
        """Establece la sección activa en la que el usuario está trabajando."""
        self.active_section = section

    def get_active_section(self):
        """Devuelve la sección activa actual."""
        return self.active_section

    def add_comment(self, section, comment):
        """Agrega un comentario a la sección especificada."""
        if section:
            if section in self.comments:
                self.comments[section].append(comment)
            else:
                self.comments[section] = [comment]
        else:
            raise ValueError("No se ha seleccionado una sección activa para agregar comentarios.")

    def get_comments(self, section=None):
        """
        Devuelve los comentarios de una sección específica.
        Si no se especifica sección, devuelve todos los comentarios.
        """
        if section:
            return self.comments.get(section, [])
        return self.comments

    def delete_comment(self, section, comment_index):
        """
        Elimina un comentario específico de una sección.
        :param section: Sección de donde se eliminará el comentario.
        :param comment_index: Índice del comentario a eliminar.
        """
        if section in self.comments and 0 <= comment_index < len(self.comments[section]):
            del self.comments[section][comment_index]

    def edit_comment(self, section, comment_index, new_comment):
        """
        Edita un comentario específico en una sección.
        :param section: Sección donde se encuentra el comentario.
        :param comment_index: Índice del comentario a editar.
        :param new_comment: Nuevo texto para reemplazar el comentario.
        """
        if section in self.comments and 0 <= comment_index < len(self.comments[section]):
            self.comments[section][comment_index] = new_comment