import streamlit as st

def render_highlight_comment_section(document_content):
    st.markdown(
        """
        <style>
        .highlight {
            background-color: yellow;
            cursor: pointer;
        }
        .comment {
            border-left: 2px solid blue;
            margin-left: 5px;
            padding-left: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "highlights" not in st.session_state:
        st.session_state["highlights"] = []
    if "comments" not in st.session_state:
        st.session_state["comments"] = []

    st.write("### Document Viewer")
    document_html = document_content
    for highlight, comment in zip(st.session_state["highlights"], st.session_state["comments"]):
        document_html = document_html.replace(
            highlight, f'<span class="highlight">{highlight}</span>'
        )
    st.markdown(document_html, unsafe_allow_html=True)

    st.text_input("Select text to highlight", key="selected_text")
    if st.button("Highlight"):
        if st.session_state.get("selected_text"):
            st.session_state["highlights"].append(st.session_state["selected_text"])
            st.session_state["comments"].append("")
            st.experimental_rerun()

    st.write("### Comments")
    for i, comment in enumerate(st.session_state["comments"]):
        st.text_area(f"Comment for: {st.session_state['highlights'][i]}", value=comment, key=f"comment_{i}")