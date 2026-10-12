# Setup and Usage Guide

## Prerequisites

Before using the GST Legal Reply Generator, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Quick Start (Using Pre-built Database)

If you are using the pre-built vector database from Google Drive, follow these steps:

1. **Clone the repository** (or download the project files)
   ```
   git clone <your-repo-url>
   cd GST
   ```

2. **Download the pre-built database from Google Drive**
   - Link: [Your Google Drive Link Here]
   - Download the `data.zip` file containing:
     - `vector_db.index` (FAISS vector index)
     - `metadata.json` (Document metadata)
   - Extract the contents to the `data/` folder in the project root

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your Groq API key to the `.env` file:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```
   - Get your API key from: https://console.groq.com

5. **Run the application**
   ```
   python run.py
   ```
   Or directly with Streamlit:
   ```
   streamlit run src/app.py
   ```

6. **Access the web interface**
   - Open your browser and navigate to: http://localhost:8501

## Building the Database from Scratch

If you want to build the vector database from source documents:

### Step 1: Download Source Documents

Run the downloader scripts to fetch GST-related PDFs:

```bash
cd src
python downloader.py        # Downloads notifications from CBIC
python judgement_d.py       # Downloads judgments from Rattan Advocates
```

Documents will be saved to:
- `gst_database/gst_english_notifications/`
- `gst_database/rattan_judgments/`

### Step 2: Process PDFs to Text

Convert downloaded PDFs to cleaned text files:

```bash
python pdf_to_text.py
```

Cleaned text files will be saved to `cleaned_pdfs/`.

### Step 3: Create Text Chunks

Split text files into manageable chunks:

```bash
python chunk_cleaned_pdfs.py
```

This creates `data/chunks.json`.

### Step 4: Build Vector Database

Generate embeddings and create the FAISS index:

```bash
python create_vector_db.py
```

This creates:
- `data/vector_db.index`
- `data/metadata.json`

Note: This step requires significant RAM (8GB+) and may take 30-60 minutes depending on your system.

## Usage

### Web Interface

1. Launch the application using `python run.py`
2. Upload a GST Show Cause Notice PDF or paste the notice text
3. Click "Generate Legal Reply"
4. The system will display a structured legal reply

### Programmatic Usage

```python
from src.rag_pipeline import generate_reply

notice_text = """Your GST notice text here..."""
reply = generate_reply(notice_text)
print(reply)
```

## Troubleshooting

### Issue: FAISS index not found
**Solution**: Ensure `vector_db.index` and `metadata.json` are in the `data/` folder.

### Issue: Groq API error
**Solution**: Check that your `GROQ_API_KEY` is correctly set in the `.env` file.

### Issue: Out of memory during embedding
**Solution**: Reduce the batch size in `create_vector_db.py` or use a machine with more RAM.

### Issue: Streamlit not found
**Solution**: Install all dependencies with `pip install -r requirements.txt`

## Google Drive Upload Instructions

To upload your `gst_database` folder to Google Drive:

1. **Compress the folder**:
   - Right-click on `gst_database` folder
   - Select "Send to > Compressed (zipped) folder" (Windows)
   - Or use: `tar -czvf gst_database.tar.gz gst_database/` (Linux/Mac)

2. **Upload to Google Drive**:
   - Open Google Drive (drive.google.com)
   - Click "New" > "File upload"
   - Select the compressed file
   - Wait for upload to complete

3. **Get shareable link**:
   - Right-click the uploaded file
   - Click "Share"
   - Change access to "Anyone with the link"
   - Copy the link

4. **Add to README**:
   - Paste the link in the README.md where it says `[Your Google Drive Link Here]`

## File Structure

```
GST/
├── data/                      # Vector database files
│   ├── vector_db.index       # FAISS index (download from Drive)
│   └── metadata.json         # Document metadata (download from Drive)
├── src/                       # Source code
│   ├── app.py                # Streamlit web interface
│   ├── rag_pipeline.py       # Core RAG logic
│   ├── create_vector_db.py   # Database builder
│   ├── chunk_cleaned_pdfs.py # Text chunking
│   ├── pdf_to_text.py        # PDF processor
│   ├── downloader.py         # Document downloader
│   └── judgement_d.py        # Judgment scraper
├── gst_database/              # Source PDFs (user-provided)
├── cleaned_pdfs/              # Processed text files
├── run.py                     # Entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git exclusions
└── README.md                  # Project documentation
```

## Support

For issues or questions, please open an issue in the GitHub repository.
