'''
problem tanımı: kullanıcının sağlıkla ilgili sorularını anlayan ve yanıtlayan bir GPT tabanlı doktor asistanı chatbot.
    - kullanıcının yasını ve adını dikkate alan cevaplar üretsin.
    - mesaj gecmişini hatırlayarak diyalogu ona göre sürdürmeli: memory
    - langchain ve OPENAI GPT
    - ilk olarak terminalde çalışacak bir versiyon ardından fastAPI tabanlı bir web servisi olusturulacak.
    - client tarafını yazıp test edelim

veri seti: veri seti yok onun yerine hazır gpt modelini kullanarak prompt ayarlaması yapalım

model tanıtımı: groq

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
        -grok ekle
        -python-dotenv: .env api anahtarını almak için kullanacağız
        

ortam değişkenlerini tanımla

LLM + memory 

kullanıcı bilgilerini al isim ve yaş

# chatbot döngüsü tanımlama

'''


from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.config import RunnableConfig
from typing import cast

# .env dosyasındaki API_KEY'i yükle
load_dotenv()

# 1. Modeli Kur (Hızlı ve ücretsiz Llama-3-8b)
llm = ChatGroq(
    model="llama-3.3-70b-versatile", # Şu anki en güncel ve zeki modellerden biri
    temperature=0.2 
)
# 2. Sistem Promptu (B2/C1 Seviyesi İngilizce Mantık ile Kurgulandı)
# Modelin adı/yaşı sorması ve geçmişi hatırlaması burada verildi.
system_prompt = """
Sen deneyimli, güvenilir ve empatik bir sağlık asistanısın.
Kullanıcının adı ve yaşı bilinmiyorsa, ilk yanıttan önce nazikçe sor.

Yanıt kuralları:
1. Kesinlikle tıbbi teşhis koyma.
2. Yanıta doğal ve kısa bir empati cümlesiyle başla. 
   Abartılı veya aşırı duygusal ifadeler kullanma. Örnek: "Bu semptomlar oldukça yorucu olabilir."
3. Kullanıcının yazdığı semptomlar arasında yüksek ateş, şiddetli ağrı, 
   nefes darlığı veya bilinç kaybı varsa doğrudan şunu yaz: 
   "Bu belirtiler acil değerlendirme gerektirebilir, lütfen en yakın sağlık kuruluşuna başvurun."
4. Olası nedenleri kısaca say, ardından yaşa uygun pratik öneriler ver.
5. Semptomların süresi bilinmiyorsa sonda bir soru sor.
6. Yanıtın son cümlesinde yalnızca bir kez, yapıcı şekilde uzman görüşü almasını öner.
7. Kısa ve net yaz. Dolgu cümle, gereksiz tekrar kullanma.
8. Kullanıcıya ismiyle hitap et, samimi ama ölçülü bir dil kullan.
9.Türkçe yaz, Türkçe dil kurallarına dikkat et.
   Tüm yanıt boyunca "siz" dilini kullan, "sen" kullanma.
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

if __name__ == "__main__":
    print("-" * 50)
    print("🩺 AI Doktor Asistanı Terminal Versiyonu")
    print("Çıkış yapmak için 'q' yazabilirsiniz.")
    print("-" * 50)

    session_id = "user_1"

    while True:
        user_input = input("\nSiz: ")
        
        if user_input.lower() in ["q", "quit", "exit"]:
            print("Sağlıklı günler dileriz, hoşça kalın!")
            break
            
        if not user_input.strip():
            continue

        config = cast(RunnableConfig, {"configurable": {"session_id": session_id}})
        response = assistant_with_history.invoke({"question": user_input}, config= config)
        
        print(f"\nAsistan: {response.content}")









