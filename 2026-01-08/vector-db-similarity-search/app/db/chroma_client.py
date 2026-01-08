import chromadb
from app.config.settings import settings

client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory=settings.CHROMA_PERSIST_DIR
    )
)

collection = client.get_or_create_collection(
    name="company_policies",
    metadata={"hnsw:space": "cosine"}
)
