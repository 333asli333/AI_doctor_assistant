import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// VITE_API_BASE boşsa istekler göreli yola gider ve üretimde nginx onları
// backend'e proxy'ler. Yerel geliştirmede nginx yok, o yüzden vite'ın kendi
// proxy'si aynı işi yapar (VITE_API_PROXY).
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const hedef = env.VITE_API_PROXY || "http://localhost:8000";

  return {
    plugins: [react()],
    server: {
      port: Number(env.VITE_DEV_PORT) || 5173,
      proxy: env.VITE_API_BASE
        ? undefined
        : {
            "/chat": { target: hedef, changeOrigin: true },
            "/health": { target: hedef, changeOrigin: true },
          },
    },
    build: { outDir: "dist", sourcemap: false },
  };
});
