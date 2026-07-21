import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()
nvidia_key = os.getenv("NVIDIA_API_KEY")

try:
    models = ChatNVIDIA.get_available_models(api_key=nvidia_key)
    for m in models:
        if "llama" in m.id.lower() and "70b" in m.id.lower():
            print("LLAMA MATCH:", m.id)
except Exception as e:
    print("Error:", e)
