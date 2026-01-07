from app.db.chroma_client import collection
from app.services.embedding_service import generate_embedding
from app.db.chroma_client import collection

# CREATE
def add_document(doc_id: str, text: str):
    embedding = generate_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[doc_id]
    )

# READ
def query_documents(query: str, n_results: int = 3):
    query_embedding = generate_embedding(query)

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

# UPDATE
def update_document(doc_id: str, new_text: str):
    new_embedding = generate_embedding(new_text)

    collection.update(
        ids=[doc_id],
        documents=[new_text],
        embeddings=[new_embedding]
    )

# DELETE
def delete_document(doc_id: str):
    collection.delete(ids=[doc_id])


def get_all_documents(limit: int = 10):
    return collection.get(
        limit=limit,
        include=["documents", "embeddings", "metadatas"]
    )
