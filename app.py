import streamlit as st
from utils.api_handler import get_model_feedback
from utils.file_processor import extract_text
import os

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
        col1, col2 = st.columns([2, 1])

        # Left Column: Document display and section navigation
        with col1:
            st.subheader("📄 Document Viewer")
            section_names = list(sections.keys())
            selected_section = st.radio("Select a section to analyze:", section_names)

            # Display the document with highlights for selected section
            for section, content in sections.items():
                if section == selected_section:
                    st.markdown(
                        f"<div style='background-color:#fdf5e6; padding:10px; border-left:5px solid #ffa500;'>"
                        f"<strong>{section}</strong><br>{content}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='padding:10px;'><strong>{section}</strong><br>{content}</div>",
                        unsafe_allow_html=True,
                    )

        # Right Column: Comments and feedback
        with col2:
            st.subheader("💬 Comments")
            if selected_section in st.session_state.comments:
                comment = st.text_area(
                    f"Comments for '{selected_section}':",
                    value=st.session_state.comments[selected_section],
                    height=200,
                )
            else:
                comment = st.text_area(
                    f"Comments for '{selected_section}':",
                    placeholder="Add your comment here...",
                    height=200,
                )

            if st.button("Save Comment", key=f"save_{selected_section}"):
                st.session_state.comments[selected_section] = comment
                st.success(f"Comment saved for section '{selected_section}'!")

            st.subheader("All Comments")
            for section, comment in st.session_state.comments.items():
                st.markdown(
                    f"<div style='background-color:#f0f8ff; padding:10px; border-left:5px solid #4682b4;'>"
                    f"<strong>{section}</strong><br>{comment}</div>",
                    unsafe_allow_html=True,
                )

        # Export Comments and Generate Review Report
        st.markdown("### 📤 Export Comments")
        if st.button("Generate Review Report"):
            try:
                report_content = generate_review_report(sections, st.session_state.comments, writing_style)
                st.download_button(
                    label="Download Review Report",
                    data=report_content,
                    file_name="review_report.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"Error generating the review report: {e}")

    except Exception as e:
        st.error(f"Error processing the document: {e}")
else:
    st.info("Please upload a document to begin analysis.")


# Generate Review Report Function
def generate_review_report(sections, comments, style):
    """
    Generates a structured review report using a predefined template.
    """
    report_lines = []
    report_lines.append("# Research Review Report\n")
    report_lines.append(f"**Writing Style Evaluated:** {style}\n")
    report_lines.append(f"**Total Sections Analyzed:** {len(sections)}\n")
    report_lines.append("\n---\n")

    for section, content in sections.items():
        report_lines.append(f"## Section: {section}\n")
        report_lines.append(content)
        report_lines.append("\n")
        if section in comments:
            report_lines.append("### Comments:\n")
            report_lines.append(comments[section])
        else:
            report_lines.append("### Comments:\nNo comments provided.\n")
        report_lines.append("\n---\n")

    report_lines.append("# End of Report\n")

    return "\n".join(report_lines)