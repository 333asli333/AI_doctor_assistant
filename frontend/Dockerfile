# --- 1. Aşama: derleme (bun) ---
FROM oven/bun:1-alpine AS build
WORKDIR /app

# Önce yalnız manifest'ler kopyalanır: kaynak değişince bağımlılık katmanı
# yeniden çözülmesin diye.
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile

COPY . .

# Tarayıcının API'ye gideceği adres derlemeye GÖMÜLÜR; değişirse restart
# yetmez, imaj yeniden derlenmeli. nginx API'yi proxy'lemediği için boş
# bırakılamaz — build arg ile başka bir adres verilebilir.
ARG VITE_API_BASE=https://doctor-assistant-api.aisli.dev
ENV VITE_API_BASE=$VITE_API_BASE
RUN test -n "$VITE_API_BASE" || (echo "VITE_API_BASE boş olamaz" && exit 1)
RUN bun run build

# --- 2. Aşama: servis (nginx) ---
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
