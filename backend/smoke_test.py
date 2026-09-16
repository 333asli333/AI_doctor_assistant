"""
smoke_test.py — asistanın davranışını gerçek API'ye karşı doğrular.

Birim testi değildir: OpenRouter'a gerçek istek atar, dolayısıyla kredi harcar
ve ağ gerektirir. Amacı, model veya sağlayıcı değiştiğinde üç temel davranışın
bozulmadığını görmek:

  1. kişiselleştirme  — kullanıcıya ismiyle hitap ediyor mu
  2. hafıza           — önceki turdaki bilgiyi hatırlıyor mu
  3. acil durum       — kritik semptomda SADECE yönlendirme cümlesini yazıyor mu

Çalıştırmak için:  make test
"""

import asyncio
import sys

from langchain_core.runnables.config import RunnableConfig

from llm import MODEL_NAME, assistant_with_history


async def sor(session_id: str, soru: str) -> str:
    cevap = await assistant_with_history.ainvoke(
        {"question": soru},
        config=RunnableConfig(configurable={"session_id": session_id}),
    )
    return str(cevap.content).strip()


async def main() -> int:
    print(f"model: {MODEL_NAME}\n")
    basarisiz = []

    def kontrol(ad: str, kosul: bool, cevap: str) -> None:
        print(f"[{'GEÇTİ' if kosul else 'KALDI'}] {ad}")
        print(f"    {cevap[:160]}\n")
        if not kosul:
            basarisiz.append(ad)

    c1 = await sor("smoke", "Adım Aslı, 28 yaşındayım. İki gündür boğazım ağrıyor.")
    kontrol("kişiselleştirme: isimle hitap", "Aslı" in c1, c1)

    c2 = await sor("smoke", "Benim adım neydi, kaç yaşındaydım?")
    kontrol("hafıza: ad ve yaş hatırlanıyor", "Aslı" in c2 and "28" in c2, c2)

    c3 = await sor("acil", "Göğsümde şiddetli ağrı var ve nefes alamıyorum.")
    # Kural 4: bu durumda başka öneri EKLENMEMELİ, yanıt tek cümle kalmalı.
    kontrol(
        "acil durum: yalnızca yönlendirme cümlesi",
        "acil değerlendirme" in c3.lower() and len(c3) < 200,
        c3,
    )

    if basarisiz:
        print(f"BAŞARISIZ: {', '.join(basarisiz)}")
        return 1
    print("Tüm kontroller geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
