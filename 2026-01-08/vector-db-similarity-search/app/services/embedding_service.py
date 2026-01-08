import requests
from app.config.settings import settings

def generate_embedding(text: str) -> list:
    payload = {
        "model": settings.EMBEDDING_MODEL,
        "prompt": text
    }

    response = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/embeddings",
        json=payload
    )

    response.raise_for_status()
    return response.json()["embedding"]
