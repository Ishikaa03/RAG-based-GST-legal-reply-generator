import os
import json
from tqdm import tqdm

INPUT_FOLDER = "cleaned_pdfs"
OUTPUT_FILE = "data/chunks.json"

CHUNK_SIZE = 800
OVERLAP = 150


def _validate_input_folder():
    """Validate input folder exists and has .txt files."""
    if not os.path.isdir(INPUT_FOLDER):
        raise FileNotFoundError(f"Input folder not found: {INPUT_FOLDER}")
    
    txt_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")]
    if not txt_files:
        raise ValueError(
            f"No .txt files found in {INPUT_FOLDER}\n"
            "Run `python pdf_to_text.py` first to generate cleaned PDFs."
        )
    return len(txt_files)


def split_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks


def process_all_files():

    all_chunks = []

    chunk_id = 0

    files = os.listdir(INPUT_FOLDER)

    for file in tqdm(files):

        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(INPUT_FOLDER, file)

        with open(file_path, "r", encoding="utf-8") as f:

            text = f.read()

        chunks = split_text(text)

        for chunk in chunks:

            all_chunks.append({
                "chunk_id": chunk_id,
                "source": file,
                "text": chunk
            })

            chunk_id += 1

    return all_chunks


if __name__ == "__main__":

    try:
        txt_count = _validate_input_folder()
        print(f"Chunking started... ({txt_count} files found)")

        chunks = process_all_files()

        print(f"Total chunks created: {len(chunks)}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

            json.dump(chunks, f, indent=2, ensure_ascii=False)

        print("Chunks saved to:", OUTPUT_FILE)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise SystemExit(1)