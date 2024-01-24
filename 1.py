import streamlit as st
from google.colab import files
import fitz  # PyMuPDF
import spacy
from tabulate import tabulate

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_information_from_pdf(pdf_path, keywords):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()

    # Process the text using spaCy
    doc = nlp(text)

    # Dictionary to store relevant information organized by keyword
    keyword_info = {}

    # Iterate through sentences to find relevant information
    for keyword in keywords:
        keyword_info[keyword] = []

        for sentence in doc.sents:
            if keyword.lower() in sentence.text.lower():
                keyword_info[keyword].append({"Context": sentence.text})

    return keyword_info

# Streamlit interface
st.title("PDF Information Extractor")

# Upload PDF file
pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

if pdf_file is not None:
    # Ask for keywords
    input_keyword = st.text_input("Enter a keyword:")

    # Button to trigger information extraction
    if st.button("Extract Information"):
        # Extract information
        keywords = [input_keyword]
        information = extract_information_from_pdf(pdf_file, keywords)

        # Display information
        if information[input_keyword]:
            st.header(f"Relevant Information for '{input_keyword}':")

            headers = ["#", "Context"]
            data = [(i + 1, info["Context"]) for i, info in enumerate(information[input_keyword])]

            st.table(tabulate(data, headers=headers, tablefmt="pretty"))
        else:
            st.warning(f"No relevant information found for the keyword '{input_keyword}'.")
