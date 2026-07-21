import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

nvidia_key = os.getenv("NVIDIA_API_KEY")

try:
    print("Testing embeddings with NVIDIA Build...")
    embeddings = OpenAIEmbeddings(
        openai_api_key=nvidia_key,
        openai_api_base="https://integrate.api.nvidia.com/v1",
        model="nvidia/nv-embedqa-e5-v5"
    )
    result = embeddings.embed_query("Prueba de embeddings")
    print(f"Success! Vector length: {len(result)}")
except Exception as e:
    print(f"Error testing NVIDIA embeddings: {e}")
