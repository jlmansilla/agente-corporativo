import os
from langchain_openai import ChatOpenAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

nvidia_key = os.getenv("NVIDIA_API_KEY")
modelo = "z-ai/glm5"
base_url = "https://integrate.api.nvidia.com/v1"

print("--- Testing con ChatOpenAI ---")
try:
    llm_openai = ChatOpenAI(
        model=modelo,
        api_key=nvidia_key,
        base_url=base_url
    )
    res1 = llm_openai.invoke("Hola, responde en una palabra.")
    print("ChatOpenAI exitoso:", res1.content)
except Exception as e:
    print(f"Error ChatOpenAI: {e}")

print("--- Testing con ChatNVIDIA ---")
try:
    llm_nvidia = ChatNVIDIA(
        model=modelo,
        nvidia_api_key=nvidia_key
    )
    res2 = llm_nvidia.invoke("Hola, responde en una palabra.")
    print("ChatNVIDIA exitoso:", res2.content)
except Exception as e:
    print(f"Error ChatNVIDIA: {e}")
