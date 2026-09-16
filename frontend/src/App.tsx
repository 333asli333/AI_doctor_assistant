import { useState } from "react";

import Onboarding, { type Kullanici } from "./components/Onboarding";
import Chat from "./components/Chat";

export default function App() {
  // Kullanıcı null iken giriş formu, dolduğunda sohbet ekranı gösterilir.
  const [kullanici, setKullanici] = useState<Kullanici | null>(null);

  return kullanici ? (
    <Chat kullanici={kullanici} onCikis={() => setKullanici(null)} />
  ) : (
    <Onboarding onTamam={setKullanici} />
  );
}
