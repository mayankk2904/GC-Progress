import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")
    CHROMA_PERSIST_DIR: str = os.path.abspath(
        os.getenv("CHROMA_PERSIST_DIR")
    )

settings = Settings()

print("CHROMA_PERSIST_DIR =", settings.CHROMA_PERSIST_DIR)
