import streamlit as st
from utils.api_handler import get_model_feedback
from utils.file_processor import extract_text
import os

# Streamlit setup
st.set_page_config(page_title="Research Assistant", layout="wide")
st.title("📝 Research Assistant with Meta-Llama")

st.markdown("""
Upload a research document to receive AI-generated feedback on:
- Writing quality
- Coherence with theory and objectives
- Suggestions for improving specific sections
""")

# File upload
uploaded_file = st.file_uploader("Upload a document (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])

if uploaded_file:
    try:
        # Extract text from the document
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
            if st.button("Analyze Section"):
                st.info("Sending the section to the AI for analysis...")
                feedback = get_model_feedback(sections[selected_section])
                st.success("Analysis complete!")
                
                # Display feedback
                st.subheader("Feedback")
                for idx, comment in enumerate(feedback, 1):
                    st.markdown(f"**{idx}.** {comment}")

    except Exception as e:
        st.error(f"Error processing the document: {e}")
else:
    st.info("Please upload a document to begin.")