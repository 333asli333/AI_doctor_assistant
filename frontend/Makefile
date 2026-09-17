# AI Doktor Asistanı — frontend
# Kullanım: make <hedef>

COMPOSE := docker compose
BUN     := bun

.DEFAULT_GOAL := help
.PHONY: help install dev build preview typecheck up down logs restart clean

help:  ## Hedefleri listele
	@grep -hE '^[a-z-]+:.*?##' $(MAKEFILE_LIST) | awk -F':.*?## ' '{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install:  ## Bağımlılıkları kur
	$(BUN) install

dev: install  ## Vite geliştirme sunucusu (backend'e proxy'ler)
	$(BUN) run dev

build: install  ## Üretim derlemesi
	$(BUN) run build

preview: build  ## Derlemeyi yerelde önizle
	$(BUN) run preview

typecheck: install  ## TypeScript denetimi
	$(BUN) run typecheck

up:  ## Konteyneri derle ve başlat
	$(COMPOSE) up -d --build

down:  ## Konteyneri durdur
	$(COMPOSE) down

restart:  ## Yeniden başlat
	$(COMPOSE) restart

logs:  ## Logları takip et
	$(COMPOSE) logs -f

clean:  ## Bağımlılıkları ve derleme çıktısını sil
	rm -rf node_modules dist
