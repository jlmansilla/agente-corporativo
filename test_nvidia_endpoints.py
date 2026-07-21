import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv

load_dotenv()

nvidia_key = os.getenv("NVIDIA_API_KEY")

try:
    print("Testing embeddings with NVIDIAEmbeddings...")
    embeddings = NVIDIAEmbeddings(
        nvidia_api_key=nvidia_key,
        model="nvidia/nv-embedqa-e5-v5"
    )
    result = embeddings.embed_query("Prueba de embeddings")
    print(f"Success! Vector length: {len(result)}")
except Exception as e:
    print(f"Error testing NVIDIA embeddings: {e}")
