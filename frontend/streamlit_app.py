import streamlit as st
import sys
import os
import urllib.request

# Add root directory to path so we can import app.rag_pipeline directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load Gemini key from Streamlit Cloud Secrets if available
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

from app.rag_pipeline import EnterpriseRAGPipeline

st.set_page_config(page_title="Enterprise RAG + Guardrails", layout="wide")
st.title("🛡️ Enterprise Document Q&A with Hallucination Guardrails")

@st.cache_resource
def load_pipeline():
    return EnterpriseRAGPipeline()

rag = load_pipeline()

with st.sidebar:
    st.header("1. Upload Knowledge Base")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if st.button("Process & Index Documents") and uploaded_files:
        with st.spinner("Chunking and embedding documents..."):
            pdf_files = [(f.name, f.getvalue()) for f in uploaded_files]
            chunks_added = rag.ingest_pdfs(pdf_files)
            st.success(f"Successfully indexed {chunks_added} chunks from {len(pdf_files)} file(s).")

    st.divider()
    st.caption("No PDF handy? Load a built-in sample paper:")
    if st.button("Load Sample RAG Paper"):
        with st.spinner("Downloading and indexing sample paper..."):
            sample_path = "sample_rag_survey.pdf"
            urllib.request.urlretrieve("https://arxiv.org", sample_path)
            with open(sample_path, "rb") as f:
                chunks_added = rag.ingest_pdfs([("RAG_Survey_Paper.pdf", f.read())])
            st.success(f"Loaded sample paper ({chunks_added} chunks)! Try asking: 'What are the three paradigms of RAG?'")

st.header("2. Ask Verified Questions")
question = st.text_input("Enter your question about the uploaded documents:")

if st.button("Get Answer") and question:
    with st.spinner("Retrieving, reranking, and verifying faithfulness..."):
        data = rag.query(question, top_k=4)
        st.subheader("Answer")
        ans = data["answer"]
        if isinstance(ans, list):
            ans = "".join([block.get("text", "") for block in ans if isinstance(block, dict)])
        st.write(ans)

        col1, col2 = st.columns(2)
        col1.metric("Faithfulness Score", f"{data['faithfulness_score']:.2f}")
        col2.metric("Grounded Check", "Passed ✅" if data["is_grounded"] else "Flagged ⚠️")

        with st.expander("View Retrieved & Reranked Sources"):
            for src in data["sources"]:
                st.markdown(f"**{src['source']} (Page {src['page']})**")
                st.caption(src["content"])
