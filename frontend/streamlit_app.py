import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Enterprise RAG + Guardrails", layout="wide")
st.title("🛡️ Enterprise Document Q&A with Hallucination Guardrails")

with st.sidebar:
    st.header("1. Upload Knowledge Base")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if st.button("Process & Index Documents") and uploaded_files:
        with st.spinner("Chunking and embedding documents..."):
            files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
            res = requests.post(f"{API_URL}/upload", files=files)
            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error(res.text)

st.header("2. Ask Verified Questions")
question = st.text_input("Enter your question about the uploaded documents:")

if st.button("Get Answer") and question:
    with st.spinner("Retrieving, reranking, and verifying faithfulness..."):
        res = requests.post(f"{API_URL}/query", json={"question": question, "top_k": 4})
        if res.status_code == 200:
            data = res.json()
            st.subheader("Answer")
            st.write(data["answer"])

            col1, col2 = st.columns(2)
            col1.metric("Faithfulness Score", f"{data['faithfulness_score']:.2f}")
            col2.metric("Grounded Check", "Passed ✅" if data["is_grounded"] else "Flagged ⚠️")

            with st.expander("View Retrieved & Reranked Sources"):
                for src in data["sources"]:
                    st.markdown(f"**{src['source']} (Page {src['page']})**")
                    st.caption(src["content"])
        else:
            st.error("Error communicating with backend API.")
