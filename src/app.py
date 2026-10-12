import streamlit as st
import fitz
from rag_pipeline import generate_reply


st.set_page_config(
    page_title="GST Legal Reply Generator",
    layout="wide"
)

st.title("GST Legal Notice Reply Generator")
st.write("Upload GST Notice PDF or paste notice text.")


# PDF text extractor
def extract_pdf_text(file):

    doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    return text


# Upload PDF
uploaded_file = st.file_uploader(
    "Upload GST Notice PDF",
    type=["pdf"]
)


# Or paste text
notice_text_input = st.text_area(
    "Or paste GST notice text here",
    height=200
)


notice_text = ""


if uploaded_file:

    notice_text = extract_pdf_text(uploaded_file)

    st.subheader("Extracted Notice Text")

    st.text_area("", notice_text, height=200)


elif notice_text_input:

    notice_text = notice_text_input


# Generate reply button
if st.button("Generate Legal Reply"):

    if not notice_text.strip():

        st.warning("Please upload or enter notice text.")

    else:

        with st.spinner("Analyzing notice and generating legal reply..."):

            reply = generate_reply(notice_text)

        st.subheader("Generated Legal Reply")

        st.write(reply)