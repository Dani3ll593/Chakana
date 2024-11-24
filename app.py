import streamlit as st
from utils.api_handler import get_model_feedback
from utils.file_processor import extract_text
import os

# Streamlit setup
st.set_page_config(page_title="Research Assistant", layout="wide")
st.title("📝 Research Assistant with Meta-Llama")

st.markdown("""
Upload a research document or paste text below to receive AI-generated feedback on:
- Writing quality
- Coherence with theory and objectives
- Suggestions for improving specific sections
""")

# File upload
uploaded_file = st.file_uploader("Upload a document (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])

# Text input
st.markdown("Or paste your text below:")
text_input = st.text_area("Paste your research text here:", height=200)

# Process document if uploaded
if uploaded_file:
    try:
        st.info("Processing the document...")
        document_text, sections = extract_text(uploaded_file)
        st.success("Document successfully processed!")

        # Section navigation
        st.subheader("Sections")
        section_names = list(sections.keys())
        selected_section = st.selectbox("Select a section for analysis:", section_names)

        if selected_section:
            st.subheader("Selected Section")
            st.write(sections[selected_section])

            # Analyze section with AI
            if st.button("Analyze Selected Section"):
                with st.spinner("Analyzing the section with AI..."):
                    feedback = get_model_feedback(sections[selected_section])
                st.success("Analysis complete!")
                st.subheader("AI Feedback")
                st.markdown(feedback)  # Display feedback as a paragraph

    except Exception as e:
        st.error(f"Error processing the document: {e}")

# Process pasted text if provided
elif text_input.strip():
    if st.button("Analyze Pasted Text"):
        with st.spinner("Analyzing the text with AI..."):
            try:
                feedback = get_model_feedback(text_input)
                st.success("Analysis complete!")
                st.subheader("AI Feedback")
                st.markdown(feedback)  # Display feedback as a paragraph
            except Exception as e:
                st.error(f"Error analyzing the text: {e}")
else:
    st.info("Please upload a document or paste text for analysis.")