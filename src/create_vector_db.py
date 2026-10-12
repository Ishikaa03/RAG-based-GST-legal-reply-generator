import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os


CHUNKS_FILE = "data/chunks.json"

INDEX_FILE = "data/vector_db.index"

METADATA_FILE = "data/metadata.json"


print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]

print(f"Total chunks loaded: {len(texts)}")


print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-large-en-v1.5")


print("Creating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)


print("Embedding shape:", embeddings.shape)


dimension = embeddings.shape[1]

print("Creating FAISS index...")

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


print("Saving vector database...")

faiss.write_index(index, INDEX_FILE)


print("Saving metadata...")

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)


print("DONE: Vector database created successfully.")