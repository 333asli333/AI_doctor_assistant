# 🩺 AI Doktor Asistanı / AI Doctor Assistant

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61dafb?logo=react)
![Vite](https://img.shields.io/badge/Vite-6-646cff?logo=vite)
![Bun](https://img.shields.io/badge/Bun-1.x-black?logo=bun)
![OpenRouter](https://img.shields.io/badge/OpenRouter-Gemini%202.5%20Flash-orange)

---

## 🇹🇷 Türkçe

### Proje Hakkında
Kullanıcının adını, yaşını ve sağlık şikayetini alarak kişiselleştirilmiş Türkçe sağlık bilgisi sunan, hafızalı bir AI doktor asistanı. OpenRouter üzerinden çalışan Google Gemini modeli, LangChain ile yönetilen konuşma hafızası ve FastAPI tabanlı bir servis ile geliştirilmiştir.

> ⚠️ Bu uygulama tıbbi teşhis koymaz. Sağlık sorunlarınız için mutlaka bir doktora danışınız.

### Özellikler
- 🧠 **Konuşma hafızası** — oturum boyunca önceki mesajları hatırlar
- 👤 **Kişiselleştirme** — kullanıcıya ismiyle hitap eder, yaşa uygun yanıt üretir
- 🚨 **Acil durum algısı** — kritik semptomlarda doğrudan acil uyarısı verir, başka öneri eklemez
- 🌐 **Web arayüzü** — giriş formu (ad, yaş, şikayet) + sohbet ekranı
- 🔒 **Oturum yönetimi** — oturumu kapat ve yeni kullanıcı başlat

### Mimari

İki bağımsız Docker kompozisyonu. SSL'i sunucudaki ters vekil bitirir.

| Parça | Yol | Host portu |
|---|---|---|
| Backend — FastAPI + LangChain | `backend/` | 8003 |
| Frontend — React + Vite + nginx | `frontend/` | 8002 |

Frontend, `/chat` ve `/health` isteklerini ortak docker ağı üzerinden backend'e proxy'ler; bu yüzden tek alan adı yeter. Ayrı bir API alan adı isterseniz `VITE_API_BASE` doldurulup **imaj yeniden derlenir** (adres derlemeye gömülür).

```
ai-doctor/
├── backend/
│   ├── llm.py            # model, prompt, zincir, hafıza
│   ├── api.py            # FastAPI (yalnız JSON)
│   ├── terminal.py       # terminal sürümü
│   ├── smoke_test.py     # davranış doğrulaması
│   ├── Dockerfile · docker-compose.yml · Makefile
│   └── .env.example
└── frontend/
    ├── src/              # React + TypeScript
    ├── Dockerfile · nginx.conf · docker-compose.yml · Makefile
    └── .env.example
```

### Kurulum

Ortak ağ bir kez oluşturulur:

```bash
docker network create ai-doctor
```

**Backend**

```bash
cd backend
cp .env.example .env      # OPENROUTER_API_KEY değerini doldurun
make up                   # derle ve başlat
make health               # {"status":"ok", ...}
```

**Frontend**

```bash
cd frontend
make up
```

Tarayıcıda `http://localhost:8002` adresini açın.

### Yerel geliştirme

Docker olmadan, iki terminalde:

```bash
cd backend  && make dev        # uvicorn :8000, canlı yeniden yükleme
cd frontend && make dev        # vite :5173, /chat isteklerini :8000'e proxy'ler
```

Terminal sürümü için: `cd backend && make terminal`

### Doğrulama

```bash
cd backend  && make test       # gerçek API'ye karşı davranış testi
cd frontend && make typecheck  # TypeScript denetimi
```

`make test` OpenRouter'a gerçek istek atar ve kredi harcar. Üç şeyi kontrol eder: isimle hitap, hafıza, acil durum yanıtının tek cümle kalması.

### Model

Varsayılan `google/gemini-2.5-flash` (~0.30$/1M token). OpenRouter'da **ücretsiz Gemini kalmadı**; daha ucuzu `google/gemini-2.5-flash-lite` (~0.10$) ama yönergeleri daha zayıf takip ediyor. Model `OPENROUTER_MODEL` ile değiştirilir.

`max_tokens` 800'e sabitlenmiştir: verilmezse OpenRouter modelin tavanını (65k) varsayıp bakiyeyi ona göre kontrol eder ve düşük bakiyede 402 döner.

### Deploy (Dokploy)

Sunucu Dokploy ile yönetilir, SSL'i ters vekil bitirir. Sunucuda elle nginx ayarı yapılmaz, certbot çalıştırılmaz.

1. **DNS (Cloudflare):** `doctor-assistant` için A kaydı → sunucu IP'si.
2. **Backend servisi:** Build type `Dockerfile`, Build path `backend/`, Environment'a `OPENROUTER_API_KEY`. Alan adı gerekmez.
3. **Frontend servisi:** Build type `Dockerfile`, Build path `frontend/`, Domain `doctor-assistant.aisli.dev`, **Container Port 80**.

İki servis de aynı docker ağında olmalı ki nginx backend'e ulaşabilsin.

---

## 🇬🇧 English

### About
A conversational AI health assistant that collects the user's name, age, and health complaint to provide personalized Turkish-language health information. Built with Google Gemini via OpenRouter, LangChain conversation memory, a FastAPI backend, and a React + Vite frontend served by nginx.

> ⚠️ This application does not provide medical diagnoses. Always consult a doctor for health concerns.

### Tech Stack
| Layer | Technology |
|---|---|
| LLM | Google Gemini (OpenRouter) |
| LLM Management | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | React + Vite + TypeScript (bun) |
| Web server | nginx |
| Deployment | Docker + Dokploy (self-hosted) |

### Quick start

```bash
docker network create ai-doctor
cd backend  && cp .env.example .env && make up
cd ../frontend && make up
```

Open `http://localhost:8002`.

Run `make help` in either folder to see all targets.

---

### Bilinen sınır / Known limitation

Sohbet hafızası süreç belleğinde (`store` sözlüğü) tutulur: konteyner yeniden başlatıldığında tüm konuşmalar silinir ve backend tek worker ile çalışmak zorundadır. Kalıcılık gerekirse bir veritabanı katmanı eklenmelidir.

---

*Built by [Aslı](https://github.com/333asli333)*
