import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v1")
API_KEY = os.getenv("AIML_API_KEY")

# Initialize OpenAI API
api = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

# Streamlit configuration
st.set_page_config(page_title="Research Text Reviewer", layout="wide")
st.title("📘 Research Text Reviewer")

# User instructions
st.markdown("""
Upload a document to get AI-generated feedback on:
- Writing quality.
- Coherence with theory.
- Alignment with research objectives.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your document (.txt only)", type=["txt"])

if uploaded_file:
    try:
        # Read file content
        text = uploaded_file.read().decode("utf-8")
        st.subheader("Uploaded Text")
        st.text_area("Preview:", text, height=300, disabled=True)

        # Process text with the AI API
        st.subheader("AI Feedback")
        if st.button("Analyze Text"):
            with st.spinner("Analyzing the text..."):
                completion = api.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an academic writing assistant. Analyze the following text and provide "
                                "feedback on writing quality, coherence with theory, and alignment with research objectives."
                            ),
                        },
                        {"role": "user", "content": text},
                    ],
                    temperature=0.7,
                    max_tokens=512,
                )
                response = completion.choices[0].message.content

            # Display the feedback
            st.success("Analysis complete!")
            st.text_area("Feedback:", response, height=300, disabled=True)

    except Exception as e:
        st.error(f"Error processing the document: {e}")
else:
    st.info("Upload a text document to get started.")