# 🩺 AI Doktor Asistanı / AI Doctor Assistant

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-yellow)
![OpenRouter](https://img.shields.io/badge/OpenRouter-Gemini%202.0%20Flash-orange)
![Deploy](https://img.shields.io/badge/Deploy-Docker%20%2B%20Dokploy-blue?logo=docker)

---

## 🇹🇷 Türkçe

### Proje Hakkında
Kullanıcının adını, yaşını ve sağlık şikayetini alarak kişiselleştirilmiş Türkçe sağlık bilgisi sunan, hafızalı bir AI doktor asistanı. OpenRouter üzerinden çalışan Google Gemini modeli, LangChain ile yönetilen konuşma hafızası ve FastAPI tabanlı web servisi ile geliştirilmiştir.

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
| LLM | Google Gemini (OpenRouter) |
| LLM Yönetimi | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Deploy | Docker + Dokploy (self-hosted) |

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
cp .env.example .env   # sonra OPENROUTER_API_KEY değerini doldurun

# Çalıştır
uvicorn api:app --reload
```

Tarayıcıda `http://localhost:8000` adresini aç.

### Ekran Görüntüleri

<!-- Ekran görüntüsü veya GIF buraya eklenecek -->
<!-- ![Demo](assets/demo.gif) -->

---

## 🚀 Deploy (Dokploy)

Sunucu Dokploy ile yönetiliyor, SSL'i ters vekil bitiriyor. **Sunucuda elle nginx
ayarı yapılmaz, certbot çalıştırılmaz.**

### 1. DNS kaydı (Cloudflare)

`aisli.dev` alan adı Cloudflare'de. DNS → Records → Add record:

| Alan | Değer |
|---|---|
| Type | `A` |
| Name | `doctor-assistant` |
| IPv4 | sunucunun IP'si (Dokploy panelinden) |
| Proxy | mevcut `aurelia` kaydıyla aynı yapılır |

Not: zone'da `*.aisli.dev → 192.168.1.1` şeklinde bir joker kayıt var; bu özel bir
adres olduğu için hiçbir yere gitmez. Her alt alan adı **açıkça** eklenmelidir.

### 2. .env

```bash
cp .env.example .env   # OPENROUTER_API_KEY değerini doldur
```

Dokploy kullanılıyorsa değişkenler panelin Environment sekmesine girilir.

### 3. Dokploy uygulaması

Panel: `https://server.aisli.dev` → Create Application

- Kaynak: GitHub → `333asli333/AI_doctor_assistant`, dal `main`
- Build type: **Dockerfile** (repo kökündeki `Dockerfile`)
- Environment: `OPENROUTER_API_KEY`, istersen `OPENROUTER_MODEL`
- Domain: `doctor-assistant.aisli.dev`, container port **8000**, HTTPS açık

Deploy'a bas. Sonrası `main`'e push → Dokploy çeker.

### Dokploy olmadan (elle compose)

```bash
cd /opt/ai-doctor && docker compose up -d --build
curl http://127.0.0.1:8002/health
```

Host portu 8002'dir; ters vekil alan adını bu porta sürer.
(8000 aurelia frontend, 8001 aurelia backend tarafından kullanılıyor.)

### Güncelleme

```bash
git push origin main      # Dokploy otomatik çeker
```

---

## 🇬🇧 English

### About
A conversational AI health assistant that collects the user's name, age, and health complaint to provide personalized Turkish-language health information. Built with Google Gemini via OpenRouter, LangChain conversation memory, and a FastAPI web service.

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
| LLM | Google Gemini (OpenRouter) |
| LLM Management | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Docker + Dokploy (self-hosted) |

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
cp .env.example .env   # sonra OPENROUTER_API_KEY değerini doldurun

# Run
uvicorn api:app --reload
```

Open `http://localhost:8000` in your browser.

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
├── .env                           # OPENROUTER_API_KEY (not committed)
├── .env.example                   # Örnek ortam değişkenleri
├── Dockerfile
├── docker-compose.yml
└── static/
    └── index.html                 # Web UI (onboarding + chat)
```

---

*Built by [Aslı](https://github.com/333asli333)*
