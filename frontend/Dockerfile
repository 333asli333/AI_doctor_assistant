# --- 1. Aşama: derleme (bun) ---
FROM oven/bun:1-alpine AS build
WORKDIR /app

# Önce yalnız manifest'ler kopyalanır: kaynak değişince bağımlılık katmanı
# yeniden çözülmesin diye.
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile

COPY . .

# Tarayıcının API'ye gideceği adres derlemeye GÖMÜLÜR; değişirse restart
# yetmez, imaj yeniden derlenmeli. Boş bırakılırsa aynı origin kullanılır ve
# aşağıdaki nginx proxy'si devreye girer.
ARG VITE_API_BASE=""
ENV VITE_API_BASE=$VITE_API_BASE
RUN bun run build

# --- 2. Aşama: servis (nginx) ---
FROM nginx:1.27-alpine
# Frontend nginx'inin istekleri taşıyacağı backend. Yerel compose'da servis
# "backend" takma adıyla bulunur; Dokploy'da backend uygulamasının App Name'i
# yazılır, ör. http://ai-doctor-backend-xxxx:8000
ENV BACKEND_URL=http://backend:8000
# templates/ altına konan dosyayı resmi imaj açılışta envsubst'ten geçirir;
# yalnız tanımlı ortam değişkenleri değişir, $host gibi nginx değişkenleri kalır.
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
