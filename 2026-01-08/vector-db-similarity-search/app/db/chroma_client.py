import chromadb
from app.config.settings import settings
import os

os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
print(f"Using ChromaDB at: {settings.CHROMA_PERSIST_DIR}")

try:
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    print("Using PersistentClient")
except Exception as e:
    print(f"Error creating PersistentClient: {e}")
    client = chromadb.Client(
        settings=chromadb.Settings(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            is_persistent=True
        )
    )
    print("Fallback to Client with persistence settings")

collection = client.get_or_create_collection(
    name="company_policies",
    metadata={"hnsw:space": "cosine"}
)

print(f"Collection '{collection.name}' ready. Count: {collection.count()}")