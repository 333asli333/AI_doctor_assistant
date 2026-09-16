import { useEffect, useRef, useState } from "react";

export type Kullanici = { ad: string; yas: string; sikayet: string };

export default function Onboarding({ onTamam }: { onTamam: (k: Kullanici) => void }) {
  const [adim, setAdim] = useState<0 | 1>(0);
  const [ad, setAd] = useState("");
  const [yas, setYas] = useState("");
  const [sikayet, setSikayet] = useState("");
  const [hata, setHata] = useState("");
  const sikayetRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (adim === 1) sikayetRef.current?.focus();
  }, [adim]);

  function ilerle() {
    if (!ad.trim() || !yas.trim()) {
      setHata("Lütfen adınızı ve yaşınızı girin.");
      return;
    }
    setHata("");
    setAdim(1);
  }

  return (
    <div id="onboardingScreen">
      <span className="onboard-icon">🩺</span>
      <h2 className="onboard-title">AI Doktor Asistanı</h2>
      <p className="onboard-subtitle">
        Size kişiselleştirilmiş sağlık bilgisi sunabilmem için önce sizi tanımak istiyorum.
      </p>

      <div className="step-indicator">
        <div className={`step-dot ${adim === 0 ? "active" : "done"}`} />
        <div className={`step-dot ${adim === 1 ? "active" : ""}`} />
      </div>

      {adim === 0 ? (
        <div className="step-content active">
          <div className="field-group">
            <label htmlFor="ad">Adınız</label>
            <input
              id="ad"
              type="text"
              placeholder="Örn. Ayşe"
              autoComplete="off"
              value={ad}
              onChange={(e) => setAd(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && ilerle()}
            />
          </div>
          <div className="field-group">
            <label htmlFor="yas">Yaşınız</label>
            <input
              id="yas"
              type="number"
              placeholder="Örn. 32"
              min={1}
              max={120}
              value={yas}
              onChange={(e) => setYas(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && ilerle()}
            />
          </div>
          {hata && <p className="field-error">{hata}</p>}
          <button className="btn-primary" onClick={ilerle}>
            Devam Et →
          </button>
        </div>
      ) : (
        <div className="step-content active">
          <div className="field-group">
            <label htmlFor="sikayet">Sağlığınızla ilgili sorunuzu belirtin</label>
            <textarea
              id="sikayet"
              ref={sikayetRef}
              className="health-textarea"
              placeholder={
                "Şikayetlerinizi veya sorularınızı kısaca yazabilirsiniz...\n\nÖrn: Son birkaç gündür baş ağrım var, ne yapmalıyım?"
              }
              value={sikayet}
              onChange={(e) => setSikayet(e.target.value)}
            />
          </div>
          <button
            className="btn-primary"
            onClick={() => onTamam({ ad: ad.trim(), yas: yas.trim(), sikayet: sikayet.trim() })}
          >
            Sohbeti Başlat →
          </button>
        </div>
      )}

      <p className="disclaimer-note">
        ⚠️ Bu araç tıbbi teşhis koymaz. Sağlık sorunlarınız için mutlaka bir doktora danışınız.
      </p>
    </div>
  );
}
