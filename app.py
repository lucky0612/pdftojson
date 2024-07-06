import streamlit as st
import fitz  # PyMuPDF
import json
import re

# Function to parse PDF and extract text
def parse_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text, pdf_document.page_count

# Function to categorize content based on headings
def categorize_content(text):
    # Define common headings and subheadings in resumes
    headings = [
        "Objective", "Summary", "Experience", "Work Experience", "Education", "Skills",
        "Projects", "Certifications", "Awards", "Languages", "Interests", "References",
        "Contact Information", "Personal Information"
    ]
    
    # Additional regex patterns for common sub-sections
    subheadings_patterns = [
        r'^(?:Skills|Skill Set|Technical Skills|Technical Proficiency|Languages|Language Proficiency):?',
        r'^(?:Experience|Professional Experience|Work Experience|Employment History|Professional Background):?',
        r'^(?:Education|Educational Background|Academic Background|Academic Qualifications|Qualifications):?',
        r'^(?:Projects|Notable Projects|Project Experience|Relevant Projects):?',
        r'^(?:Certifications|Certifications & Licenses|Licenses|Professional Certifications):?',
        r'^(?:Awards|Honors|Achievements|Accomplishments):?',
        r'^(?:Languages|Language Skills):?',
        r'^(?:Interests|Hobbies|Personal Interests):?',
        r'^(?:References|Referees):?'
    ]

    subheadings_regex = re.compile('|'.join(subheadings_patterns), re.IGNORECASE)
    
    # Split text into lines
    lines = text.split('\n')

    categorized_content = {}
    current_heading = "Other"
    categorized_content[current_heading] = []

    # Regex pattern to match headings
    heading_pattern = re.compile(r'\b(?:' + '|'.join(headings) + r')\b', re.IGNORECASE)

    for line in lines:
        # Check if the line matches any heading
        if heading_pattern.search(line):
            current_heading = heading_pattern.search(line).group()
            categorized_content[current_heading] = []
        elif subheadings_regex.match(line):
            current_heading = subheadings_regex.match(line).group()
            categorized_content[current_heading] = []
        categorized_content[current_heading].append(line.strip())

    return categorized_content

# Streamlit UI
st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86C1;
        text-align: center;
        margin-top: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #117A65;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f9f9f9;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    .uploaded-file {
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar contents
st.sidebar.title("Resume Parser")
st.sidebar.info("Upload a resume in PDF format, and this tool will extract its content and present it as JSON.")

# Main title and subtitle
st.markdown("<h1 class='main-header'>Resume Parser 📄</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Upload your resume in PDF format to extract its contents as JSON.</h2>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Display placeholder image if no file is uploaded
if uploaded_file is None:
    st.image("placeholder.png", width=300, caption="Upload a PDF to get started", use_column_width=True)

# Process and display the uploaded PDF
if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    with st.spinner('Parsing PDF...'):
        raw_text, num_pages = parse_pdf(uploaded_file)
        categorized_content = categorize_content(raw_text)
    
    # Generate summary information
    num_words = len(raw_text.split())
    num_sections = len(categorized_content)
    
    st.sidebar.subheader("PDF Summary")
    st.sidebar.markdown(f"**Number of Pages:** {num_pages}")
    st.sidebar.markdown(f"**Number of Words:** {num_words}")
    st.sidebar.markdown(f"**Number of Sections:** {num_sections}")
    
    st.markdown("<h2 class='sub-header'>Parsed Content</h2>", unsafe_allow_html=True)
    
    # Display content
    for heading, content in categorized_content.items():
        st.subheader(heading)
        for line in content:
            st.text(line)
    
    # Option to download JSON
    json_data = json.dumps(categorized_content, indent=4)
    st.download_button("Download JSON", json_data, file_name="parsed_resume.json", mime="application/json")

# Footer
st.markdown("""
    <div class="footer">
        Developed with ❤ by Lakshya Raj Vijay
    </div>
    """, unsafe_allow_html=True)