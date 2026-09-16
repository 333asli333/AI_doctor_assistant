# AI Doktor Asistanı — backend
# Kullanım: make <hedef>.  Ön koşul: .env dosyası (bkz. .env.example)

COMPOSE := docker compose
VENV    := .venv
PY      := $(VENV)/bin/python

.DEFAULT_GOAL := help
.PHONY: help venv dev terminal up down logs restart shell health test clean

help:  ## Hedefleri listele
	@grep -hE '^[a-z-]+:.*?##' $(MAKEFILE_LIST) | awk -F':.*?## ' '{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

venv:  ## Yerel sanal ortamı kur
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip
	$(PY) -m pip install --quiet -r requirements.txt

dev: venv  ## Yerelde canlı yeniden yüklemeyle çalıştır
	$(VENV)/bin/uvicorn api:app --reload --port 8000

terminal: venv  ## Terminal sürümünü çalıştır
	$(PY) terminal.py

net:  ## Ortak docker ağını oluştur (bir kez)
	-docker network create ai-doctor

up: net  ## Konteyneri derle ve başlat
	$(COMPOSE) up -d --build

down:  ## Konteyneri durdur
	$(COMPOSE) down

restart:  ## Yeniden başlat
	$(COMPOSE) restart

logs:  ## Logları takip et
	$(COMPOSE) logs -f

shell:  ## Konteyner içinde kabuk aç
	$(COMPOSE) exec backend sh

health:  ## Sağlık kontrolü
	@curl -fsS http://localhost:$${AI_DOCTOR_BACKEND_PORT:-8003}/health && echo

test: venv  ## Uçtan uca duman testi (gerçek API çağrısı yapar)
	$(PY) smoke_test.py

clean:  ## Sanal ortamı ve derleme artıklarını sil
	rm -rf $(VENV) __pycache__ .pytest_cache
