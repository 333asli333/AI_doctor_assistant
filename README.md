# 🩺 AI Doktor Asistanı / AI Doctor Assistant

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-yellow)
![Groq](https://img.shields.io/badge/Groq-Llama3.3--70B-orange)
![Deploy](https://img.shields.io/badge/Deploy-Railway-purple?logo=railway)

---

## 🇹🇷 Türkçe

### Proje Hakkında
Kullanıcının adını, yaşını ve sağlık şikayetini alarak kişiselleştirilmiş Türkçe sağlık bilgisi sunan, hafızalı bir AI doktor asistanı. Groq üzerinde çalışan Llama 3.3 70B modeli, LangChain ile yönetilen konuşma hafızası ve FastAPI tabanlı web servisi ile geliştirilmiştir.

> ⚠️ Bu uygulama tıbbi teşhis koymaz. Sağlık sorunlarınız için mutlaka bir doktora danışınız.

### Özellikler
- 🧠 **Konuşma hafızası** — oturum boyunca önceki mesajları hatırlar
- 👤 **Kişiselleştirme** — kullanıcıya ismiyle hitap eder, yaşa uygun yanıt üretir
- 🚨 **Acil durum algısı** — kritik semptomlarda (göğüs ağrısı, nefes darlığı vb.) doğrudan acil uyarısı verir
- 🌐 **Web arayüzü** — giriş formu (ad, yaş, şikayet) + sohbet ekranı
- 🔒 **Oturum yönetimi** — oturumu kapat ve yeni kullanıcı başlat

### Teknoloji Stack
| Katman | Teknoloji |
|---|---|
| LLM | Llama 3.3 70B (Groq) |
| LLM Yönetimi | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Deploy | Railway |

### Kurulum

```bash
# Repoyu klonla
git clone https://github.com/333asli333/AI_doctor_assistant.git
cd AI_doctor_assistant

# Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyası oluştur
echo GROQ_API_KEY=your_key_here > .env

# Çalıştır
uvicorn api:app --reload
```

Tarayıcıda `http://localhost:8000` adresini aç.

### Canlı Demo
🔗 [aidoctorassistant-production.up.railway.app](https://aidoctorassistant-production.up.railway.app)

### Ekran Görüntüleri

<!-- Ekran görüntüsü veya GIF buraya eklenecek -->
<!-- ![Demo](assets/demo.gif) -->

---

## 🇬🇧 English

### About
A conversational AI health assistant that collects the user's name, age, and health complaint to provide personalized Turkish-language health information. Built with Llama 3.3 70B on Groq, LangChain conversation memory, and a FastAPI web service.

> ⚠️ This application does not provide medical diagnoses. Always consult a doctor for health concerns.

### Features
- 🧠 **Conversation memory** — remembers previous messages within a session
- 👤 **Personalization** — addresses users by name, tailors responses by age
- 🚨 **Emergency detection** — triggers immediate emergency warning for critical symptoms (chest pain, shortness of breath, etc.)
- 🌐 **Web interface** — onboarding form (name, age, complaint) + chat screen
- 🔒 **Session management** — logout and start a new session

### Tech Stack
| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B (Groq) |
| LLM Management | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Railway |

### Installation

```bash
# Clone the repo
git clone https://github.com/333asli333/AI_doctor_assistant.git
cd AI_doctor_assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_key_here > .env

# Run
uvicorn api:app --reload
```

Open `http://localhost:8000` in your browser.

### Live Demo
🔗 [aidoctorassistant-production.up.railway.app](https://aidoctorassistant-production.up.railway.app)

### Screenshots

<!-- Add screenshot or GIF here -->
<!-- ![Demo](assets/demo.gif) -->

---

## Project Structure

```
AI_doctor_assistant/
├── doctor_assistant_terminal.py   # LLM + LangChain core (model, memory, chain)
├── api.py                         # FastAPI web service
├── requirements.txt
├── .env                           # GROQ_API_KEY (not committed)
└── static/
    └── index.html                 # Web UI (onboarding + chat)
```

---

*Built by [Aslı](https://github.com/333asli333)*
