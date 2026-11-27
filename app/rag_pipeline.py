import os
import tempfile
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from sentence_transformers import CrossEncoder
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

class GradeOutput(BaseModel):
    score: float = Field(description="Faithfulness score between 0.0 and 1.0")
    is_grounded: bool = Field(description="True if answer is strictly supported by context")

class EnterpriseRAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)

        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.vector_store = Chroma(
            collection_name="enterprise_docs",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )
        self.all_chunks = []

    def ingest_pdfs(self, uploaded_files: List[tuple]) -> int:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        new_docs = []

        for filename, file_bytes in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = filename
                doc.metadata["page"] = doc.metadata.get("page", 0) + 1
            new_docs.extend(splitter.split_documents(docs))
            os.remove(tmp_path)

        if new_docs:
            self.vector_store.add_documents(new_docs)
            self.all_chunks.extend(new_docs)

        return len(new_docs)

    def retrieve_and_rerank(self, query: str, top_k: int = 4):
        vector_retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k * 2})

        if self.all_chunks:
            bm25_retriever = BM25Retriever.from_documents(self.all_chunks)
            bm25_retriever.k = top_k * 2
            retriever = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=[0.6, 0.4]
            )
            candidates = retriever.invoke(query)
        else:
            candidates = vector_retriever.invoke(query)

        if not candidates:
            return []

        pairs = [[query, doc.page_content] for doc in candidates]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(scores, candidates), key=lambda x: x, reverse=True)
        return [doc for _, doc in ranked[:top_k]]

    def evaluate_faithfulness(self, context: str, answer: str) -> GradeOutput:
        grader = self.llm.with_structured_output(GradeOutput)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a strict fact-checker. Verify if the Answer is 100% supported by the Context. Do not allow outside knowledge."),
            ("human", "Context:\n{context}\n\nAnswer:\n{answer}")
        ])
        chain = prompt | grader
        return chain.invoke({"context": context, "answer": answer})

    def query(self, question: str, top_k: int = 4) -> dict:
        docs = self.retrieve_and_rerank(question, top_k=top_k)
        if not docs:
            return {
                "answer": "No relevant documents found. Please upload PDFs first.",
                "faithfulness_score": 0.0,
                "is_grounded": False,
                "sources": []
            }

        context = "\n\n".join(
            [f"[{d.metadata['source']} - Page {d.metadata['page']}]: {d.page_content}" for d in docs]
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the question using ONLY the provided context. Cite sources as [Filename - Page X]. If the answer is not in the context, say 'I cannot find this information in the provided documents.'"),
            ("human", "Context:\n{context}\n\nQuestion: {question}")
        ])
        response = (prompt | self.llm).invoke({"context": context, "question": question})
        answer_text = response.content

        grade = self.evaluate_faithfulness(context, answer_text)
        if not grade.is_grounded or grade.score < 0.7:
            answer_text = f"⚠️ [Low Confidence Warning - Score: {grade.score:.2f}] {answer_text}"

        sources = [
            {
                "source": d.metadata["source"],
                "page": d.metadata["page"],
                "content": d.page_content[:250] + "..."
            }
            for d in docs
        ]

        return {
            "answer": answer_text,
            "faithfulness_score": grade.score,
            "is_grounded": grade.is_grounded,
            "sources": sources
        }
