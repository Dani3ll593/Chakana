import streamlit as st
from utils.api_handler import get_model_feedback
from utils.file_processor import extract_text
import os
import json

# Streamlit setup
st.set_page_config(page_title="Research Assistant", layout="wide")
st.title("📝 Research Assistant with Meta-Llama")

# Comment storage
if "comments" not in st.session_state:
    st.session_state.comments = {}

# File upload
uploaded_file = st.file_uploader("Upload a document (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])

# Writing style selection
st.markdown("### Select Writing Style")
writing_style = st.selectbox("Choose the style for evaluation:", ["APA", "Chicago", "Vancouver", "None"])

if uploaded_file:
    try:
        # Process the document
        document_text, sections = extract_text(uploaded_file)
        st.success("Document successfully processed!")
        
        # Layout with two columns
        col1, col2 = st.columns([1, 1])

        # Left Column: Document display and section navigation
        with col1:
            st.subheader("📄 Document Sections")
            section_names = list(sections.keys())
            selected_section = st.radio("Select a section to analyze:", section_names)

            if selected_section:
                st.write(f"### {selected_section}")
                st.write(sections[selected_section])

                # Analyze section
                if st.button("Analyze Selected Section"):
                    with st.spinner("Analyzing the section with AI..."):
                        feedback = get_model_feedback(sections[selected_section], writing_style=writing_style)
                    st.success("Analysis complete!")
                    
                    # Save feedback as the default comment
                    st.session_state.comments[selected_section] = feedback
                    st.info("The AI feedback has been saved as the default comment.")

        # Right Column: Comments and feedback
        with col2:
            st.subheader("💬 Comments")
            if selected_section in st.session_state.comments:
                comment = st.text_area(
                    f"Comments for '{selected_section}':",
                    value=st.session_state.comments[selected_section],
                    height=300,
                )

                if st.button("Save Comment"):
                    st.session_state.comments[selected_section] = comment
                    st.success("Comment saved!")

            st.subheader("All Comments")
            for section, comment in st.session_state.comments.items():
                st.markdown(f"**{section}**")
                st.write(comment)

        # Export Comments
        st.markdown("### 📤 Export Comments")
if st.button("Generate Review Report"):
    try:
        # Generate the review report
        report_content = generate_review_report(sections, st.session_state.comments, writing_style)
        st.success("Review report generated successfully!")
        
        # Provide a download button for the report
        st.download_button(
            label="Download Review Report",
            data=report_content,
            file_name="review_report.txt",
            mime="text/plain",
        )
    except Exception as e:
        st.error(f"Error generating the review report: {e}")

else:
    st.info("Please upload a document to begin analysis.")

# Generate Review Report
def generate_review_report(sections, comments, style):
    """
    Generates a review report by combining document sections with their corresponding comments.
    """
    report_lines = []
    report_lines.append("### Review Report\n")
    report_lines.append(f"**Writing Style Evaluated:** {style}\n")
    report_lines.append("\n")

    for section, content in sections.items():
        report_lines.append(f"#### {section}\n")
        report_lines.append(content)
        report_lines.append("\n")
        if section in comments:
            report_lines.append("**Comments:**\n")
            report_lines.append(comments[section])
        else:
            report_lines.append("**Comments:** None provided.\n")
        report_lines.append("\n---\n")

    return "\n".join(report_lines)

def generate_review_report(sections, comments, style):
    """
    Generates a structured review report using a predefined template.

    Parameters:
        - sections (dict): A dictionary where keys are section titles and values are the content.
        - comments (dict): A dictionary where keys are section titles and values are comments.
        - style (str): The selected writing style for evaluation.

    Returns:
        - str: The generated report as a single text string.
    """
    # Start the report with metadata
    report_lines = []
    report_lines.append("# Research Review Report\n")
    report_lines.append(f"**Writing Style Evaluated:** {style}\n")
    report_lines.append(f"**Total Sections Analyzed:** {len(sections)}\n")
    report_lines.append("\n---\n")

    # Add each section and its comments
    for section, content in sections.items():
        report_lines.append(f"## Section: {section}\n")
        report_lines.append(content)
        report_lines.append("\n")

        # Include comments for the section
        if section in comments:
            report_lines.append("### Comments:\n")
            report_lines.append(comments[section])
        else:
            report_lines.append("### Comments:\nNo comments provided.\n")
        report_lines.append("\n---\n")

    # Conclude the report
    report_lines.append("# End of Report\n")

    return "\n".join(report_lines)
