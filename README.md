# GST Legal Reply Generator

An AI-powered assistant for drafting professional legal replies to GST Show Cause Notices. Upload a notice PDF or paste the text, and receive a structured, legally sound reply generated using RAG (Retrieval-Augmented Generation) technology.

## What This Project Does

This tool helps GST advocates and taxpayers draft comprehensive replies to GST notices in minutes instead of hours. It combines semantic search over a curated legal knowledge base with LLM-powered generation to produce replies that include case facts, legal submissions, supporting precedents, and closing requests formatted according to standard GST practice.

## How to Use (Quick Start)

### 1. Get the Pre-built Database

Download the vector database from Google Drive: https://drive.google.com/drive/folders/1OmBkKoRNqxToOmNE-rd68EzxJncZ9yET?usp=drive_link

Extract the files (`vector_db.index` and `metadata.json`) into the `data/` folder.

### 2. Set Up Your API Key

1. Copy `.env.example` to `.env`:
   ```
   copy .env.example .env
   ```

2. Get your free API key from https://console.groq.com

3. Paste it in the `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

**Security Note**: Your `.env` file is automatically excluded from Git via `.gitignore`. Never commit your API key.

### 3. Install and Run

```bash
pip install -r requirements.txt
python run.py
```

Then open http://localhost:8501 in your browser.

### 4. Generate a Reply

1. Upload your GST notice PDF OR paste the notice text
2. Click "Generate Legal Reply"
3. Copy the structured reply for professional use

## How It Works

1. **Retrieval**: Your notice text is embedded and matched against a vector database of GST judgments, circulars, and notifications using FAISS similarity search
2. **Generation**: Retrieved legal context is fed to Groq's Llama 3.3 70B model with a carefully engineered prompt that structures replies into Facts, Submissions, Supporting Precedents, and Requests
3. **Output**: A complete, formatted legal reply ready for review and submission

## Building from Scratch (Optional)

If you want to build the knowledge base yourself:

```bash
cd src
python downloader.py         # Download notifications
python judgement_d.py          # Download judgments
python pdf_to_text.py          # Extract text from PDFs
python chunk_cleaned_pdfs.py   # Create text chunks
python create_vector_db.py     # Build vector index (requires 8GB+ RAM, ~30 min)
```

## Project Structure

```
GST/
├── data/              # Vector database (download from Drive)
├── src/               # Source code
│   ├── app.py         # Web interface
│   ├── rag_pipeline.py # Core RAG logic
│   └── ...            # Data processing scripts
├── gst_database/      # Source PDFs (not in repo)
├── run.py             # Launch command
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## System Requirements

- Python 3.8+
- 8GB RAM (for database building)
- Groq API key (free tier available)

## Important Disclaimer

This tool assists with drafting but does not replace qualified legal counsel. Always review generated content with a practicing GST advocate before submission. Verify all citations, case laws, and statutory references independently.

## Data Sources

The knowledge base includes judgments under Sections 73 and 74 of the CGST Act, CBIC circulars, GST Council notifications, and other statutory materials from official government sources.
