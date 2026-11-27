# 🚀 Live Deployment & Visual Walkthrough (`DEMO.md`)

🔗 **Live Deployed App:** [https://enterprise-rag-guardrails-hktaezgdgpqpchtvxhvbag.streamlit.app](https://enterprise-rag-guardrails-hktaezgdgpqpchtvxhvbag.streamlit.app)

This visual guide walks through deploying the **Enterprise RAG with Hallucination Guardrails** application to Streamlit Community Cloud and running real-time document Q&A.

---

## Step 1: Open Streamlit Community Cloud Workspace
Sign in with GitHub (`dinesh-916`) and click **Create app** to start a new cloud deployment.

<img width="955" height="479" alt="Screenshot 2026-11-27 224239" src="https://github.com/user-attachments/assets/1e8a34cd-e747-4107-95d6-588d9f709e3d" />


---

## Step 2: Select Public GitHub Repository Deployment
Choose **Deploy a public app from GitHub** to link your repository directly for automated builds.

<img width="959" height="473" alt="Screenshot 2026-11-27 224303" src="https://github.com/user-attachments/assets/0ffd90e1-c28a-4ac3-903a-fcf7b7663eab" />


---

## Step 3: Configure Repository, Main File & API Secrets
Select `Dinesh-916/enterprise-rag-guardrails` (`main` branch), set the main file path to `frontend/streamlit_app.py`, add your `GOOGLE_API_KEY` in **Advanced settings**, and click **Deploy**.

<img width="833" height="467" alt="Screenshot 2026-11-27 224344" src="https://github.com/user-attachments/assets/2929dd87-a57e-4c37-83d4-9ecdf8b486ab" />

---

## Step 4: Automated Container Build & Dependency Setup
Streamlit Cloud automatically provisions the environment and installs `langchain`, `chromadb`, `sentence-transformers`, `rank-bm25`, and `pypdf`.

<img width="959" height="509" alt="Screenshot 2026-11-27 225812" src="https://github.com/user-attachments/assets/d7c768c3-3daf-4165-988a-553a9b330281" />


---

## Step 5: Live Application Interface Ready
Once provisioning completes, the web UI launches with the **Upload Knowledge Base** sidebar on the left and the **Ask Verified Questions** panel on the right.

<img width="959" height="508" alt="Screenshot 2026-11-27 225925" src="https://github.com/user-attachments/assets/08fc0df1-b4ec-4a74-94c4-a803b1739d7a" />


---

## Step 6: Upload PDF & Query with Hallucination Guardrails
1. Upload a research paper (`2312.10997v5.pdf`) in the left sidebar and click **Process & Index Documents**.
2. Ask a multi-concept question (*"What are the three main paradigms of Retrieval-Augmented Generation, and how do they differ?"*) and click **Get Answer** to view the grounded response.

<img width="959" height="509" alt="Screenshot 2026-11-27 232027" src="https://github.com/user-attachments/assets/ab5224f2-097d-4f98-80ed-72a83143ad44" />

