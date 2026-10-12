import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()


INDEX_FILE = "data/vector_db.index"
METADATA_FILE = "data/metadata.json"


print("Loading vector database...")

index = faiss.read_index(INDEX_FILE)

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)


print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-large-en-v1.5")


print("Connecting to Groq...")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve(query, top_k=8):

    query_embedding = model.encode([query])

    D, I = index.search(query_embedding, top_k)

    results = []

    for idx in I[0]:
        results.append(metadata[idx])

    return results


def generate_reply(notice_text):

    docs = retrieve(notice_text)

    context = "\n\n".join([
        f"Source: {doc['source']}\n{doc['text']}"
        for doc in docs
    ])

    prompt = fprompt = fprompt = f"""
You are a Senior GST Advocate drafting a formal reply to a Show Cause Notice (SCN) / GST Notice.

Your responsibility is to independently analyze the notice, apply relevant statutory provisions, and draft a professional reply in a structured format.

You may use:
• The retrieved legal context (if relevant)
• Your legal reasoning ability
• Applicable statutory provisions, rules, circulars, and judicial precedents

NOTICE CONTENT:
{notice_text}

RELEVANT LEGAL CONTEXT (if any):
{context}

IMPORTANT:
Do NOT mention “retrieved documents”, “database”, or any internal sources.
Draft as if you are independently researching and preparing the reply as a practicing GST Advocate.

-------------------------------------------------

STRICT FORMAT TO FOLLOW

-------------------------------------------------

From:
[Assessee Name / Director Name]
[Company Name]
[Registered Address]

To:
[Designation of Officer]
[Department Name]
[Division / Commissionerate]

Subject: Reply to Show Cause Notice No. ____ dated ____

-------------------------------------------------

Facts of the Case:

Provide a short and concise summary (5–7 lines) explaining:
• Nature of the notice
• Allegations raised
• Amount demanded (if mentioned)
• Sections invoked

Keep it clear and neutral.

-------------------------------------------------

Our Submission:

1. First Legal Issue:
Provide one well-structured paragraph rebutting the first allegation.
Mention exact Section and sub-section numbers (e.g., Section 16(2), Section 73(1)).
Explain why invocation is legally unsustainable.

2. Second Legal Issue:
Provide one strong paragraph addressing procedural defects, limitation, jurisdictional errors, or incorrect application of law (if applicable).

3. Interest and Penalty:
If invoked, analyze:
• Whether Section 50 interest is applicable
• Whether proceedings fall under Section 73 or Section 74
• Whether ingredients of fraud, suppression, or wilful misstatement exist
• Limitation period applicability

4. Additional Legal Clarification (if required):
Clarify compliance position, documentation maintained, or legal interpretation.

Keep total submission points between 3–4 strong arguments only.
Each point must be legally reasoned, structured, and persuasive.

-------------------------------------------------

Supporting:

Mention relevant:
• Judicial precedents (Supreme Court / High Court / Tribunal)
• GST Circulars
• Notifications
• Statutory provisions

Briefly explain how each supports the assessee’s case.
Do not fabricate case laws.

-------------------------------------------------

Our Request:

Draft a detailed and persuasive closing request including:

• A clear request to drop the proceedings.
• A request for waiver of interest and penalty.
• Statement that there was no fraud, suppression, or wilful misstatement.
• Mention adherence to principles of natural justice.
• Request for personal hearing.
• A respectful but firm assertion that demand is legally unsustainable.
• Any other relief deemed fit under law.

This section must be convincing, professionally worded, and 8–10 lines long.

-------------------------------------------------

Place: [City Name]
Date: [Current Date]

Yours Faithfully,
[Authorized Signatory Name]
[Designation]

-------------------------------------------------

DRAFTING RULES:

• Maintain strong but respectful legal tone.
• Avoid overly technical AI-style language.
• Avoid repeating the notice verbatim.
• Use structured paragraphs.
• Cite statutory provisions precisely.
• Ensure the “Our Request” section is persuasive and detailed.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content