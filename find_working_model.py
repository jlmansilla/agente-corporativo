import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()
nvidia_key = os.getenv("NVIDIA_API_KEY")

try:
    models = ChatNVIDIA.get_available_models(api_key=nvidia_key)
    for m in models[:15]: # check the first 15 models to find a working one
        print(f"Testing model: {m.id}")
        try:
            llm = ChatNVIDIA(model=m.id, nvidia_api_key=nvidia_key)
            res = llm.invoke("Hola")
            print(f"SUCCESS: {m.id}")
            break
        except Exception as e:
            print(f"FAILED {m.id}: {e}")
except Exception as e:
    print("Error:", e)
