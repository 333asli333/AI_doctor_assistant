"""
Birim testleri için ortak kurulum.

llm.py içe aktarılırken OPENROUTER_API_KEY arar ve yoksa hata verir. Testler
gerçek API'ye hiç gitmez; anahtar yalnız içe aktarma kontrolünü geçmek için
sahte bir değerle doldurulur. LLM çağrıları testlerde sahte modelle değiştirilir.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("OPENROUTER_API_KEY", "test-anahtari-gercek-degil")
os.environ.setdefault("FRONTEND_URL", "")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
