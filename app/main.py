from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from app.schemas import QueryRequest, QueryResponse
from app.rag_pipeline import EnterpriseRAGPipeline

app = FastAPI(title="Enterprise RAG with Hallucination Guardrails")
rag = EnterpriseRAGPipeline()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    pdf_files = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        content = await file.read()
        pdf_files.append((file.filename, content))

    chunks_added = rag.ingest_pdfs(pdf_files)
    return {"message": f"Successfully indexed {chunks_added} chunks from {len(pdf_files)} file(s)."}

@app.post("/query", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    return rag.query(request.question, request.top_k)
