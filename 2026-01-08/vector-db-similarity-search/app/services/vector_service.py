from app.db.chroma_client import collection
from app.services.embedding_service import generate_embedding
from app.db.chroma_client import collection
import re

DEFAULT_N_RESULTS = 5
DEFAULT_MAX_DISTANCE = 0.25



def chunk_text(text: str):
    # Split by numbered sections like "1. Purpose", "2. Annual Leave"
    sections = re.split(r"\n\d+\.\s+", text)

    chunks = []
    for section in sections:
        cleaned = section.strip()
        if len(cleaned) > 50:  # ignore tiny chunks
            chunks.append(cleaned)

    return chunks



# CREATE
def add_document(doc_id: str, text: str):
    chunks = chunk_text(text)

    embeddings = []
    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        embeddings.append(generate_embedding(chunk))
        chunk_id = f"{doc_id}_chunk_{i}"
        ids.append(chunk_id)
        metadatas.append({"doc_id": doc_id, "chunk_id": chunk_id})

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas  # store the chunk IDs in metadata
    )



# READ
def query_documents(
    query: str,
    n_results: int = DEFAULT_N_RESULTS,
    max_distance: float = DEFAULT_MAX_DISTANCE
):
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "distances"]
    )

    response = []

    documents = results["documents"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    for doc_id, doc, distance in zip(ids, documents, distances):
        if distance <= max_distance:
            response.append({
                "chunk_id": doc_id,
                "content": doc,
                "distance": round(distance, 4),
                "similarity_score": round(1 - distance, 4)
            })

    return {
        "query": query,
        "results": response
    }

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
