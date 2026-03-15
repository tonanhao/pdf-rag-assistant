"""
RAG Server - Port 8000
- Embeddings: sentence-transformers (local, no API key needed)
- LLM Chat:   Google Gemini via langchain-google-genai
"""

import os
import shutil
from pathlib import Path
from typing import List

from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings

load_dotenv()

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(title="RAG AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
FAISS_INDEX_DIR = BASE_DIR / "faiss_index"
FAISS_INDEX_DIR.mkdir(exist_ok=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Global state
vector_store = None
current_pdf_name: str | None = None
_embeddings: "LocalEmbeddings | None" = None


# ── Local Embeddings ──────────────────────────────────────────────────────────
class LocalEmbeddings(Embeddings):
    """
    Offline embeddings using sentence-transformers.
    Model 'all-MiniLM-L6-v2': ~80MB, fast, no API key required.
    Auto-downloaded on first run.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"[Embeddings] Loading '{model_name}'...")
        self._model = SentenceTransformer(model_name)
        print("[Embeddings] Model ready ✓")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self._model.encode([text], show_progress_bar=False)[0].tolist()


def get_embeddings() -> LocalEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = LocalEmbeddings()
    return _embeddings


# ── LLM helpers ───────────────────────────────────────────────────────────────
FALLBACK_MODELS = [
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
]


def get_llm(model_name: str = "gemini-2.0-flash-lite") -> ChatGoogleGenerativeAI:
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY chưa được cấu hình trong file .env")
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
        max_retries=1,
    )


def invoke_with_fallback(prompt: str) -> str:
    """Try each Gemini model in order; skip on 429 quota errors."""
    last_error = None
    for model_name in FALLBACK_MODELS:
        try:
            print(f"[LLM] Trying {model_name}...")
            response = get_llm(model_name).invoke(prompt)
            print(f"[LLM] ✓ {model_name}")
            return response.content
        except Exception as e:
            msg = str(e)
            if "429" in msg or "quota" in msg.lower() or "ResourceExhausted" in msg:
                print(f"[LLM] {model_name} quota exceeded → next")
                last_error = e
            else:
                raise
    raise last_error or ValueError("All Gemini models exhausted.")


# ── Request / Response schemas ────────────────────────────────────────────────
class QueryRequest(BaseModel):
    query: str


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "RAG AI Server running on port 8000"}


@app.get("/status")
async def status():
    return {
        "status": "running",
        "pdf_loaded": current_pdf_name is not None,
        "current_pdf": current_pdf_name,
        "api_key_configured": bool(GOOGLE_API_KEY),
    }


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, current_pdf_name

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF")
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY chưa cấu hình trong backend/.env")

    # Save PDF to disk
    pdf_path = UPLOAD_DIR / file.filename
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Load & split
        documents = PyPDFLoader(str(pdf_path)).load()
        if not documents:
            raise HTTPException(status_code=400, detail="Không đọc được nội dung PDF")

        chunks = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        ).split_documents(documents)

        # Build FAISS index
        emb = get_embeddings()
        vector_store = FAISS.from_documents(chunks, emb)
        vector_store.save_local(str(FAISS_INDEX_DIR))
        current_pdf_name = file.filename

        print(f"[upload_pdf] '{file.filename}' → {len(chunks)} chunks ✓")
        return {
            "message": f"PDF '{file.filename}' đã được xử lý thành công!",
            "filename": file.filename,
            "chunks": len(chunks),
            "pages": len(documents),
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý PDF: {str(e)}")


@app.post("/ask")
async def ask_question(request: QueryRequest):
    global vector_store

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống")
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY chưa cấu hình")

    # Load FAISS from disk if not in memory
    if vector_store is None and (FAISS_INDEX_DIR / "index.faiss").exists():
        try:
            vector_store = FAISS.load_local(
                str(FAISS_INDEX_DIR),
                get_embeddings(),
                allow_dangerous_deserialization=True,
            )
            print("[/ask] Loaded FAISS from disk ✓")
        except Exception as e:
            print(f"[/ask] Cannot load FAISS: {e}")

    # No PDF — general AI answer
    if vector_store is None:
        try:
            answer = invoke_with_fallback(request.query)
            return {
                "answer": answer,
                "sources": [],
                "note": "Chưa có PDF. Đây là câu trả lời chung từ AI.",
            }
        except Exception as e:
            import traceback; traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Lỗi AI: {str(e)}")

    # RAG — retrieve + generate
    try:
        docs = vector_store.as_retriever(search_kwargs={"k": 4}).invoke(request.query)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = (
            "Sử dụng các đoạn tài liệu sau để trả lời câu hỏi một cách chính xác và đầy đủ.\n"
            "Nếu câu trả lời không có trong tài liệu, hãy nói rõ điều đó.\n\n"
            f"Tài liệu tham khảo:\n{context}\n\n"
            f"Câu hỏi: {request.query}\n\nCâu trả lời:"
        )

        print(f"[/ask] Query: {request.query[:80]}")
        answer = invoke_with_fallback(prompt)
        print(f"[/ask] Answer OK ({len(answer)} chars)")

        sources = []
        for doc in docs:
            info = {
                "page": doc.metadata.get("page", "N/A"),
                "source": doc.metadata.get("source", current_pdf_name or "Unknown"),
                "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
            }
            if info not in sources:
                sources.append(info)

        return {"answer": answer, "sources": sources[:3]}

    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý câu hỏi: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rag_server:app", host="0.0.0.0", port=8000, reload=True)
