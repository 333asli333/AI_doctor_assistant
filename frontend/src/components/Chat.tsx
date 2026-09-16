import { useEffect, useRef, useState } from "react";

import { mesajGonder, yeniOturumId } from "../api";
import type { Kullanici } from "./Onboarding";

type Mesaj = { rol: "user" | "bot"; metin: string; saat: string };

const saatSimdi = () =>
  new Date().toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" });

export default function Chat({
  kullanici,
  onCikis,
}: {
  kullanici: Kullanici;
  onCikis: () => void;
}) {
  const [mesajlar, setMesajlar] = useState<Mesaj[]>([]);
  const [yaziyor, setYaziyor] = useState(false);
  const [girdi, setGirdi] = useState("");

  // Oturum kimliği bileşenin ömrü boyunca sabit kalmalı: backend sohbet
  // geçmişini bu anahtarla saklıyor, her render'da değişirse hafıza kopar.
  const oturumId = useRef(yeniOturumId());
  const akisRef = useRef<HTMLDivElement>(null);
  const girdiRef = useRef<HTMLTextAreaElement>(null);
  const acilisGonderildi = useRef(false);

  async function gonder(metin: string) {
    setMesajlar((o) => [...o, { rol: "user", metin, saat: saatSimdi() }]);
    setYaziyor(true);
    try {
      const yanit = await mesajGonder(metin, oturumId.current);
      setMesajlar((o) => [...o, { rol: "bot", metin: yanit, saat: saatSimdi() }]);
    } catch (err) {
      const aciklama = err instanceof Error ? err.message : String(err);
      setMesajlar((o) => [
        ...o,
        { rol: "bot", metin: `⚠️ Sunucuya bağlanılamadı.\n${aciklama}`, saat: saatSimdi() },
      ]);
    } finally {
      setYaziyor(false);
      girdiRef.current?.focus();
    }
  }

  // Açılış mesajı: asistan adı, yaşı ve şikayeti ilk turda öğrensin diye
  // kullanıcı adına otomatik gönderilir. StrictMode geliştirmede efektleri
  // iki kez çalıştırdığı için bayrakla tekilleştiriyoruz.
  useEffect(() => {
    if (acilisGonderildi.current) return;
    acilisGonderildi.current = true;
    const tanitim = kullanici.sikayet
      ? `Merhaba, adım ${kullanici.ad}, yaşım ${kullanici.yas}. Şikayetim: ${kullanici.sikayet}`
      : `Merhaba, adım ${kullanici.ad}, yaşım ${kullanici.yas}.`;
    void gonder(tanitim);
  }, []);

  useEffect(() => {
    akisRef.current?.scrollTo({ top: akisRef.current.scrollHeight, behavior: "smooth" });
  }, [mesajlar, yaziyor]);

  function gonderTiklandi() {
    const metin = girdi.trim();
    if (!metin || yaziyor) return;
    setGirdi("");
    void gonder(metin);
  }

  function cikisYap() {
    if (confirm("Oturumu kapatmak istediğinizden emin misiniz?")) onCikis();
  }

  return (
    <div id="chatScreen">
      <div className="chat-header">
        <div className="chat-header-icon">🩺</div>
        <div className="chat-header-info">
          <h1>AI Doktor Asistanı</h1>
          <p>
            <span className="status-dot" />
            Çevrimiçi · <span>{kullanici.ad}</span>
          </p>
        </div>
        <button className="logout-btn" onClick={cikisYap}>
          Oturumu Kapat
        </button>
      </div>

      <div className="disclaimer-bar">
        ⚠️ Tıbbi teşhis konulmaz. Bulgularınız için bir uzmana danışınız.
      </div>

      <div className="messages" ref={akisRef}>
        {mesajlar.map((m, i) => (
          <div key={i} className={`message ${m.rol}`}>
            {/* React metni kaçırdığı için model çıktısı HTML olarak yorumlanmaz. */}
            <div className="bubble">
              {m.metin.split("\n").map((satir, j) => (
                <span key={j}>
                  {satir}
                  {j < m.metin.split("\n").length - 1 && <br />}
                </span>
              ))}
            </div>
            <span className="ts">{m.saat}</span>
          </div>
        ))}

        {yaziyor && (
          <div className="typing show">
            <span />
            <span />
            <span />
          </div>
        )}
      </div>

      <div className="input-area">
        <div className="input-row">
          <textarea
            ref={girdiRef}
            id="messageInput"
            placeholder="Sorunuzu yazın..."
            rows={1}
            value={girdi}
            onChange={(e) => {
              setGirdi(e.target.value);
              e.target.style.height = "auto";
              e.target.style.height = Math.min(e.target.scrollHeight, 110) + "px";
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                gonderTiklandi();
              }
            }}
          />
          <button className="send-btn" onClick={gonderTiklandi} disabled={yaziyor}>
            <svg viewBox="0 0 24 24">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          </button>
        </div>
        <p className="input-hint">Enter → gönder &nbsp;·&nbsp; Shift+Enter → yeni satır</p>
      </div>
    </div>
  );
}
