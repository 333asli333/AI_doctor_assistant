// VITE_API_BASE boşsa göreli yol kullanılır: üretimde nginx, geliştirmede
// vite proxy'si isteği backend'e taşır. Ayrı alan adı gerekiyorsa derleme
// sırasında doldurulur.
const TABAN = import.meta.env.VITE_API_BASE ?? "";

export type SohbetYaniti = { reply: string };

/**
 * Backend'e bir mesaj gönderir.
 *
 * Backend hata durumunda {detail: "..."} döndürür; bu metin kullanıcıya
 * gösterilebilecek Türkçe bir açıklamadır, o yüzden ham durum kodu yerine
 * onu yükseltiyoruz.
 */
export async function mesajGonder(mesaj: string, oturumId: string): Promise<string> {
  const yanit = await fetch(`${TABAN}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: mesaj, session_id: oturumId }),
  });

  if (!yanit.ok) {
    const govde = (await yanit.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(govde?.detail || `Sunucu hatası: ${yanit.status}`);
  }

  const veri = (await yanit.json()) as SohbetYaniti;
  return veri.reply;
}

export function yeniOturumId(): string {
  return "session_" + Math.random().toString(36).slice(2, 10);
}
