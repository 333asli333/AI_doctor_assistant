"""
api.py — FastAPI katmanı
Mevcut doctor_chatbot.py dosyasını değiştirmeden import eder.
Çalıştırmak için: uvicorn api:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Mevcut chatbot modülünü import et (doctor_chatbot.py adını kendi dosya adınla değiştir)
from doctor_assistant_terminal import assistant_with_history
from langchain_core.runnables.config import RunnableConfig

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
    config = RunnableConfig(configurable={"session_id": request.session_id})
    response = assistant_with_history.invoke(
        {"question": request.message},
        config=config
    )
    return ChatResponse(reply=response.content)

# --- Static dosyaları serve et ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")
