"""Zincir, hafıza ve sistem promptu.

Hafıza testleri gerçek RunnableWithMessageHistory yapısını kullanır; yalnızca
model, sırayla hazır yanıt veren sahte bir sohbet modeliyle değiştirilir.
"""

import asyncio
import os

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

import llm

ACIL_CUMLE = "Bu belirtiler acil değerlendirme gerektirebilir, lütfen en yakın sağlık kuruluşuna hemen başvurun."


def sahte_zincir(yanitlar):
    """llm.py'deki zincirin aynısı; model yerine sahte model."""
    return RunnableWithMessageHistory(
        llm.prompt | FakeListChatModel(responses=yanitlar),
        llm.get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )


def sor(zincir, oturum, soru):
    config = RunnableConfig(configurable={"session_id": oturum})
    return asyncio.run(zincir.ainvoke({"question": soru}, config=config)).content


def test_model_ayarlari():
    # OPENROUTER_MODEL verilmemişse varsayılan Gemini 2.5 Flash
    if "OPENROUTER_MODEL" not in os.environ:
        assert llm.MODEL_NAME == "google/gemini-2.5-flash"
    assert llm.llm.max_tokens == 800  # 402 bakiye hatasını önleyen tavan
    assert llm.llm.openai_api_base == "https://openrouter.ai/api/v1"


def test_ayni_oturum_ayni_gecmisi_dondurur():
    llm.store.clear()
    assert llm.get_session_history("a") is llm.get_session_history("a")
    assert llm.get_session_history("a") is not llm.get_session_history("b")


def test_hafiza_turlar_arasinda_birikir_ve_modele_gonderilir():
    llm.store.clear()
    zincir = sahte_zincir(["Adınız ve yaşınız nedir?", "Teşekkürler Deneme."])

    assert sor(zincir, "s1", "Başım ağrıyor") == "Adınız ve yaşınız nedir?"
    assert sor(zincir, "s1", "Deneme, 30") == "Teşekkürler Deneme."

    mesajlar = llm.store["s1"].messages
    assert [type(m) for m in mesajlar] == [HumanMessage, AIMessage, HumanMessage, AIMessage]
    assert mesajlar[0].content == "Başım ağrıyor"
    assert mesajlar[2].content == "Deneme, 30"


def test_oturumlar_birbirinin_gecmisini_gormez():
    llm.store.clear()
    zincir = sahte_zincir(["bir", "iki"])
    sor(zincir, "kullanici-1", "Adım Ayşe")
    sor(zincir, "kullanici-2", "Adım Mehmet")

    assert [m.content for m in llm.store["kullanici-1"].messages] == ["Adım Ayşe", "bir"]
    assert [m.content for m in llm.store["kullanici-2"].messages] == ["Adım Mehmet", "iki"]


def test_prompt_gecmisi_sistem_ile_soru_arasina_yerlestirir():
    gecmis = [HumanMessage(content="önceki soru"), AIMessage(content="önceki yanıt")]
    mesajlar = llm.prompt.invoke({"history": gecmis, "question": "yeni soru"}).to_messages()

    assert mesajlar[0].type == "system"
    assert [m.content for m in mesajlar[1:]] == ["önceki soru", "önceki yanıt", "yeni soru"]


def test_sistem_promptu_guvenlik_kurallarini_icerir():
    p = " ".join(llm.system_prompt.split())  # satır sonları kelimeleri bölmesin
    assert ACIL_CUMLE in p
    for belirti in ("göğüs ağrısı", "nefes darlığı", "bilinç kaybı", "yüksek ateş"):
        assert belirti in p
    assert "Teşhis koyma" in p
    assert "doz önerme" in p
    # acil durum kuralı diğer tüm kurallardan önce gelir
    assert p.index("ACİL DURUM") < p.index("YAPABİLECEKLERİN") < p.index("SOHBET KURALLARI")
