from typing import List
import re
import os

from langchain_community.document_loaders import PyMuPDFLoader


INPUT_FOLDER = "gst_database"
OUTPUT_FOLDER = "cleaned_pdfs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def clean_pdf_text(text: str) -> str:

    # Remove page numbers
    text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', text, flags=re.IGNORECASE)

    # Remove standalone numbers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # Remove footnote markers like 1,2,3 at line start
    text = re.sub(r'\n\d+\s', '\n', text)

    # Remove repeated whitespace
    text = re.sub(r'\s+', ' ', text)

    # Fix broken line endings
    text = re.sub(r'(?<!\.)\n', ' ', text)

    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)

    return text.strip()


def process_pdf_to_single_file(pdf_path: str):

    print("Processing:", pdf_path)

    loader = PyMuPDFLoader(pdf_path)
    pages = loader.load()

    full_text = ""

    for page in pages:

        cleaned = clean_pdf_text(page.page_content)

        if len(cleaned) > 50:
            full_text += cleaned + "\n\n"


    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    output_file = os.path.join(
        OUTPUT_FOLDER,
        base_name + "_cleaned.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)

    print("Saved:", output_file)


def process_folder():

    for file in os.listdir(INPUT_FOLDER):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(INPUT_FOLDER, file)

            process_pdf_to_single_file(pdf_path)


if __name__ == "__main__":

    process_folder()