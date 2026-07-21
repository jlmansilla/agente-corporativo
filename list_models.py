import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()
nvidia_key = os.getenv("NVIDIA_API_KEY")

try:
    models = ChatNVIDIA.get_available_models(api_key=nvidia_key)
    for m in models:
        if "glm" in m.id.lower() or "z.ai" in m.id.lower():
            print("MATCH:", m.id)
    print("Total models:", len(models))
except Exception as e:
    print("Error:", e)
