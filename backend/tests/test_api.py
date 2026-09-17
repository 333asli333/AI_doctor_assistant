"""HTTP katmanı: sağlık kontrolü, istek doğrulama, hata yönetimi.

Gerçek model yerine api.assistant_with_history sahte bir nesneyle değiştirilir;
böylece testler ağ ve kredi gerektirmez.
"""

import pytest
from fastapi.testclient import TestClient

import api


class SahteYanit:
    def __init__(self, content):
        self.content = content


class SahteAsistan:
    """ainvoke çağrılarını kaydeder ve sabit bir yanıt döndürür."""

    def __init__(self, yanit="Merhaba Deneme, nasıl yardımcı olabilirim?", hata=None):
        self.yanit = yanit
        self.hata = hata
        self.cagrilar = []

    async def ainvoke(self, girdi, config=None):
        self.cagrilar.append((girdi, config))
        if self.hata:
            raise self.hata
        return SahteYanit(self.yanit)


@pytest.fixture
def client():
    return TestClient(api.app)


@pytest.fixture
def sahte(monkeypatch):
    asistan = SahteAsistan()
    monkeypatch.setattr(api, "assistant_with_history", asistan)
    return asistan


def test_health_modeli_bildirir(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "model": api.MODEL_NAME}


def test_chat_yaniti_dondurur_ve_oturumu_iletir(client, sahte):
    r = client.post("/chat", json={"message": "Başım ağrıyor", "session_id": "abc"})
    assert r.status_code == 200
    assert r.json() == {"reply": sahte.yanit}

    girdi, config = sahte.cagrilar[0]
    assert girdi == {"question": "Başım ağrıyor"}
    assert config["configurable"]["session_id"] == "abc"


def test_chat_oturum_verilmezse_varsayilan_kullanilir(client, sahte):
    client.post("/chat", json={"message": "Merhaba"})
    _, config = sahte.cagrilar[0]
    assert config["configurable"]["session_id"] == "default_session"


@pytest.mark.parametrize("mesaj", ["", "   ", "\n\t"])
def test_bos_mesaj_modele_gitmeden_reddedilir(client, sahte, mesaj):
    r = client.post("/chat", json={"message": mesaj})
    assert r.status_code == 400
    assert r.json()["detail"] == "Mesaj boş olamaz."
    assert sahte.cagrilar == []


def test_mesaj_alani_eksikse_422(client, sahte):
    r = client.post("/chat", json={"session_id": "abc"})
    assert r.status_code == 422
    assert sahte.cagrilar == []


def test_model_hatasi_kullaniciya_anlasilir_503_olarak_doner(client, monkeypatch):
    monkeypatch.setattr(api, "assistant_with_history", SahteAsistan(hata=RuntimeError("402 kota")))
    r = client.post("/chat", json={"message": "Merhaba"})
    assert r.status_code == 503
    detay = r.json()["detail"]
    assert "ulaşılamıyor" in detay
    assert "402" not in detay  # teknik ayrıntı kullanıcıya sızmaz


def test_yanit_icerigi_metne_cevrilir(client, monkeypatch):
    monkeypatch.setattr(api, "assistant_with_history", SahteAsistan(yanit=42))
    r = client.post("/chat", json={"message": "Merhaba"})
    assert r.json() == {"reply": "42"}
