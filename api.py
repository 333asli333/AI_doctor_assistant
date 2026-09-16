"""
api.py — FastAPI katmanı
Mevcut doctor_assistant_terminal.py dosyasını değiştirmeden import eder.
Çalıştırmak için: uvicorn api:app --reload
"""

import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Mevcut chatbot modülünü import et
from doctor_assistant_terminal import assistant_with_history
from langchain_core.runnables.config import RunnableConfig

logger = logging.getLogger("ai-doctor")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="AI Doktor Asistanı")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response Modelleri ---
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    reply: str

# --- Chat Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Mesaj boş olamaz.")

    config = RunnableConfig(configurable={"session_id": request.session_id})
    try:
        response = await assistant_with_history.ainvoke(
            {"question": request.message},
            config=config
        )
    except Exception as exc:
        # Ücretsiz modelde kota/limit hataları sık görülebilir; kullanıcıya
        # teknik detay yerine anlaşılır bir mesaj döndürüyoruz.
        logger.exception("LLM çağrısı başarısız oldu")
        raise HTTPException(
            status_code=503,
            detail="Asistana şu anda ulaşılamıyor. Lütfen birazdan tekrar deneyin.",
        ) from exc

    return ChatResponse(reply=str(response.content))

# --- Sağlık kontrolü (deploy platformları için) ---
@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Static dosyaları serve et ---
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
