<div id="comments-panel">
    <h3>Comentarios</h3>
    {% for comment in comments %}
    <div class="comment">
        <div class="user">{{ comment.user }}</div>
        <div class="timestamp">{{ comment.timestamp }}</div>
        <div class="text">{{ comment.text }}</div>
    </div>
    {% endfor %}
</div>