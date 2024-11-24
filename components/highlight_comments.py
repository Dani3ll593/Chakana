import streamlit as st

def render_highlight_comment_section(document_content):
    st.write("### Highlight and Comment")
    if "highlighted_text" not in st.session_state:
        st.session_state['highlighted_text'] = []
        st.session_state['comments'] = []

    text_to_highlight = st.text_area("Document Viewer", document_content, height=300)
    if st.button("Highlight"):
        selection = st.text_input("Enter text to highlight:")
        if selection in text_to_highlight:
            st.session_state['highlighted_text'].append(selection)
            st.write(f"Highlighted: {selection}")
    
    if st.button("Add Comment"):
        comment = st.text_area("Enter your comment:")
        if comment:
            st.session_state['comments'].append(comment)
            st.write(f"Comment added: {comment}")