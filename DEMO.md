# 🚀 Live Deployment & Visual Walkthrough (`DEMO.md`)

🔗 **Try the Live App:** [https://enterprise-rag-guardrails-hktaezgdgpqpchtvxhvbag.streamlit.app](https://enterprise-rag-guardrails-hktaezgdgpqpchtvxhvbag.streamlit.app)

This walkthrough demonstrates how the application is deployed from GitHub to Streamlit Community Cloud and how end users interact with the RAG pipeline.

---

## Step 1: Connect GitHub Repository to Streamlit Cloud
Select **Deploy a public app from GitHub** from the Streamlit Cloud workspace to link the repository directly for continuous deployment.


<img width="959" height="507" alt="Screenshot 2026-11-27 220030" src="https://github.com/user-attachments/assets/1c06f64a-2e0a-4160-a07a-0e2181bb9e21" />

---

## Step 2: Configure Repository, Branch & API Secrets
Specify `Dinesh-916/enterprise-rag-guardrails` on the `main` branch, point the main file path to `frontend/streamlit_app.py`, and configure `GOOGLE_API_KEY` inside **Advanced settings**.

![Step 2 - Configure App Settings](step2_app_settings.png)

---

## Step 3: Automated Dependency Installation & Build
Streamlit Cloud automatically provisions the container, installs all dependencies (`langchain`, `chromadb`, `sentence-transformers`, `rank-bm25`), and launches the server.

![Step 3 - Build and Provisioning](step3_app_building.png)

---

## Step 4: Upload PDF & Query with Hallucination Guardrails
1. Upload a research PDF (`2312.10997v5.pdf`) in the left sidebar and click **Process & Index Documents** to chunk and embed it into ChromaDB + BM25.
2. Enter a question (*"What are the three main paradigms of Retrieval-Augmented Generation, and how do they differ?"*) and click **Get Answer** to receive a grounded response with source citations and a faithfulness score.

![Step 4 - Live Question & Answer Output](step4_live_output.png)
