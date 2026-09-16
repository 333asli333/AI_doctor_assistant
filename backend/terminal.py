"""
terminal.py — asistanın terminal sürümü.

LLM zinciri ve hafıza llm.py'de durur; burası yalnızca konsol döngüsüdür.
Çalıştırmak için:  python terminal.py
"""

from typing import cast

from langchain_core.runnables.config import RunnableConfig

from llm import assistant_with_history

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
