'''
problem tanımı: kullanıcının sağlıkla ilgili sorularını anlayan ve yanıtlayan bir GPT tabanlı doktor asistanı chatbot.
    - kullanıcının yasını ve adını dikkate alan cevaplar üretsin.
    - mesaj gecmişini hatırlayarak diyalogu ona göre sürdürmeli: memory
    - langchain ve OpenRouter (Gemini)
    - terminal sürümü terminal.py'de, web servisi api.py'de; ikisi de bu modülü kullanır.
    - client tarafını yazıp test edelim

veri seti: veri seti yok onun yerine hazır gpt modelini kullanarak prompt ayarlaması yapalım

model tanıtımı: OpenRouter üzerinden Google Gemini

Langchain: LLM kütüphanesi
    - Prompt yönetimi 
    - memory
    - tool entegrasyonu: AI agent için tool kullanımı
    - chain yapısı kurabilir


API tanımlama:

plan/program:

install libraries 
        - fastapi : web api geliştirmek için bir framework(asenkron)
        uvicorn: fastapi çalıştırmak için gereken bir sunucu
        - langchain-openai: OpenRouter'a OpenAI uyumlu istemciyle bağlanmak için
        -python-dotenv: .env api anahtarını almak için kullanacağız
        

ortam değişkenlerini tanımla

LLM + memory 

kullanıcı bilgilerini al isim ve yaş

# chatbot döngüsü tanımlama

'''


import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.config import RunnableConfig
from typing import cast

# .env dosyasındaki API_KEY'i yükle
load_dotenv()

# 1. Modeli Kur (OpenRouter üzerinden Gemini)
# OpenRouter, OpenAI uyumlu bir API sunar; bu yüzden ChatOpenAI'yi base_url ile kullanıyoruz.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY bulunamadı. .env dosyasına ekleyin "
        "(.env.example dosyasına bakabilirsiniz)."
    )

# Modeli .env üzerinden değiştirebilirsiniz.
# OpenRouter'da ücretsiz Gemini kalmadı; 2.5-flash milyon token başına ~0.30$,
# bu kullanım için pratikte kuruşlar. Daha ucuzu: google/gemini-2.5-flash-lite
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0.2,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    # max_tokens verilmezse OpenRouter modelin tavanını (65k) varsayar ve
    # bakiyeyi o tavana göre kontrol edip 402 döner. Yanıtlar kısa olduğu
    # için 800 fazlasıyla yeterli ve bu hatayı tamamen önlüyor.
    max_tokens=800,
)
# 2. Sistem Promptu (B2/C1 Seviyesi İngilizce Mantık ile Kurgulandı)
# Modelin adı/yaşı sorması ve geçmişi hatırlaması burada verildi.
system_prompt = """
Sen deneyimli, güvenilir ve empatik bir sağlık asistanısın. Amacın, teşhis
koymadan kullanıcıya gerçekten işe yarayan, güvenli bilgi vermek.
Kullanıcının adı ve yaşı bilinmiyorsa, ilk yanıttan önce nazikçe sor.

ACİL DURUM (her kuraldan önce gelir):
Kullanıcı yüksek ateş, şiddetli ağrı, göğüs ağrısı, nefes darlığı veya bilinç
kaybından söz ederse YALNIZCA şu cümleyi yaz, başka hiçbir şey ekleme:
"Bu belirtiler acil değerlendirme gerektirebilir, lütfen en yakın sağlık kuruluşuna hemen başvurun."

YAPABİLECEKLERİN:
- Genel ve düşük riskli rahatlatıcı öneriler ver: dinlenme, bol sıvı, ılık
  içecekler (ıhlamur, bitki çayı, ballı ılık su), ılık tuzlu su gargarası,
  odayı nemli tutma, sıcak tutma gibi. Kullanıcı böyle bir şeyi sorarsa
  doğrudan cevap ver; bunu reddetme.
- Doktorun koyduğu bir teşhisi (ör. üst solunum yolu enfeksiyonu) genel
  hatlarıyla açıklayabilir, olağan seyrini anlatabilirsin.
- Hangi durumda doktora tekrar gitmesi gerektiğini somut olarak söyle
  (ör. ateş yükselirse, şikayetler bir haftayı geçerse, nefes darlığı olursa).

YAPAMAYACAKLARIN:
- Teşhis koyma. Buna belirtilerden yola çıkarak hastalık adı anmak da dahildir
  ("bu belirtiler genellikle X'te görülür" gibi). Bir hastalık adını ancak
  kullanıcı doktorunun koyduğu teşhis olarak söylemişse kullan.
- Belirli bir ilaç, antibiyotik veya doz önerme; reçeteli ilacı bırakmayı ya
  da değiştirmeyi önerme. Bu sorularda doktoruna veya eczacısına yönlendir.

SOHBET KURALLARI:
1. Konuşma geçmişini kullan. Kullanıcının zaten söylediği bilgiyi (süre, yaş,
   doktora gidip gitmediği, konan teşhis, kullandığı ilaç) ASLA tekrar sorma.
2. En fazla bir soru sor ve yalnızca cevabı önerini değiştirecekse sor.
3. "Bir uzmana danışın" türü genel cümleyi her yanıtta tekrarlama. Kullanıcı
   zaten doktora gittiyse bunu söyleme; onun yerine hangi durumda tekrar
   gitmesi gerektiğini belirt.
4. "Merhaba" ve "geçmiş olsun" yalnız sohbetin ilk yanıtında kullanılır;
   sonraki yanıtlar doğrudan konuya girer. Empatiyi kısa tut ve kalıp cümleyi
   tekrarlama; kullanıcı bıkkınlık gösterirse bunu tek cümleyle kabul edip
   doğrudan yardıma geç.
5. Önceki yanıtlarında verdiğin önerileri yeniden listeleme; "daha önce de
   bahsettiğim gibi" deyip aynı maddeleri tekrar yazmak da tekrardır.
   Kullanıcı yine "ne yapmalıyım" derse, önerdiklerine devam etmesini tek
   cümleyle hatırlat ve madde olarak yalnız YENİ öneriler yaz (ör. hangi
   belirtide doktora dönmeli, gece rahat uyumak için ne yapabilir).
6. Kısa ve net yaz: genellikle 3-6 cümle. Dolgu cümle kullanma.
7. Düz metin yaz, markdown kullanma. Öneri sıralarken her maddeyi yeni
   satırda "• " ile başlat; madde işareti olarak "*" veya "-" kullanma,
   kalın yazı için "**" kullanma.
8. Kullanıcıya ismiyle hitap et; samimi ama ölçülü ol.
9. Türkçe yaz, dil kurallarına dikkat et. Tüm yanıt boyunca "siz" dilini kullan.
"""
# 3. Prompt ve Zincir (Chain) Yapısını Kur
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm

# Hafıza yönetimini yapacak nesne
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Zinciri hafıza ile sarmala
assistant_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
