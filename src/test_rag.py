from rag_pipeline import generate_reply

query = """
GST notice issued for ITC mismatch under Section 16 CGST Act
"""

reply = generate_reply(query)

print(reply)