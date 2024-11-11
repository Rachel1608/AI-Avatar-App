import streamlit as st
import PyPDF2
import docx
import spacy
import re

# Load Spacy model for NLP tasks
nlp = spacy.load('en_core_web_sm')

# Functions to handle PDF and DOCX file extraction
def extract_pdf_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    return text

def extract_docx_text(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s.]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Named entity recognition function
def perform_ner(text):
    doc = nlp(text)
    entities = {'characters': set(), 'locations': set(), 'dates': set(), 'organizations': set()}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities['characters'].add(ent.text)
        elif ent.label_ == "GPE":
            entities['locations'].add(ent.text)
        elif ent.label_ == "DATE":
            entities['dates'].add(ent.text)
        elif ent.label_ == "ORG":
            entities['organizations'].add(ent.text)
    return entities

# Streamlit UI
st.title("AI Text Generator")

uploaded_file = st.file_uploader("Upload a .pdf or .docx file", type=["pdf", "docx"])

if uploaded_file is not None:
    # Extract text from uploaded file
    if uploaded_file.type == "application/pdf":
        text = extract_pdf_text(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_docx_text(uploaded_file)

    # Show extracted text
    st.subheader("Extracted Text")
    st.write(text)

    # Clean and preprocess text
    cleaned_text = clean_text(text)
    st.subheader("Cleaned Text")
    st.write(cleaned_text)

    # Perform NER and display entities
    entities = perform_ner(cleaned_text)
    st.subheader("Extracted Entities")
    st.write(f"Characters: {', '.join(entities['characters'])}")
    st.write(f"Locations: {', '.join(entities['locations'])}")
    st.write(f"Dates: {', '.join(entities['dates'])}")
    st.write(f"Organizations: {', '.join(entities['organizations'])}")

    # Generate summary
    st.subheader("Generated Summary for the uploaded file")
    summary = f"The story revolves around {', '.join(entities['characters'])}"
    if entities['locations']:
        summary += f" in locations like {', '.join(entities['locations'])}."
    if entities['dates']:
        summary += f" The events take place during {', '.join(entities['dates'])}."
    if entities['organizations']:
        summary += f" Key organizations involved include {', '.join(entities['organizations'])}."
    st.write(summary)
