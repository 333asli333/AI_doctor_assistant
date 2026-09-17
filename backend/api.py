"""
api.py — FastAPI katmanı.

LLM zinciri ve hafıza llm.py'de tanımlıdır; burası yalnızca HTTP katmanıdır.
Arayüz ayrı bir serviste (frontend/) durur ve buraya ağ üzerinden bağlanmaz;
tarayıcı bu servise doğrudan gelir. Bu servis yalnız JSON konuşur.
Çalıştırmak için: uvicorn api:app --reload
"""

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm import MODEL_NAME, assistant_with_history
from langchain_core.runnables.config import RunnableConfig

logger = logging.getLogger("ai-doctor")

app = FastAPI(title="AI Doktor Asistanı")

# Frontend ayrı bir serviste ve ayrı bir alan adında; tarayıcı API'ye başka
# bir origin'den geldiği için CORS şart. Üretimde FRONTEND_URL doldurulur ve
# izin yalnız ona verilir; boşsa hepsine izin verilir ki yerel geliştirmede
# vite sunucusu engellenmesin.
FRONTEND_URL = os.getenv("FRONTEND_URL", "").strip()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Mesaj boş olamaz.")

    config = RunnableConfig(configurable={"session_id": request.session_id})
    try:
        response = await assistant_with_history.ainvoke(
            {"question": request.message},
            config=config,
        )
    except Exception as exc:
        # Kota/limit hataları olabildiğince sık görülür; kullanıcıya teknik
        # detay yerine anlaşılır bir mesaj döndürüyoruz.
        logger.exception("LLM çağrısı başarısız oldu")
        raise HTTPException(
            status_code=503,
            detail="Asistana şu anda ulaşılamıyor. Lütfen birazdan tekrar deneyin.",
        ) from exc

    return ChatResponse(reply=str(response.content))


@app.get("/health")
async def health():
    """Ters vekil ve konteyner sağlık kontrolü için."""
    return {"status": "ok", "model": MODEL_NAME}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
