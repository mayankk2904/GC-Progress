from app.services.embedding_service import generate_embedding
from app.db.chroma_client import collection, client

import re

DEFAULT_N_RESULTS = 5
DEFAULT_MAX_DISTANCE = 0.25



def chunk_text(text: str):
    sections = re.split(r"\n\d+\.\s+", text)

    chunks = []
    for section in sections:
        cleaned = section.strip()
        if cleaned:
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
        metadatas=metadatas
    )
    
    # REMOVE THIS LINE - PersistentClient doesn't need explicit persist()
    # client.persist()
    
    print(f"✅ Added {len(chunks)} chunks for document {doc_id}")
    print(f"✅ Vector count:", collection.count())

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
    results = collection.get(where={"doc_id": doc_id})
    old_ids = results["ids"]

    collection.delete(ids=old_ids)
    add_document(doc_id, new_text)


# DELETE
def delete_document(doc_id: str):
    results = collection.get(where={"doc_id": doc_id})
    collection.delete(ids=results["ids"])


def get_all_documents(limit: int = 10):
    return collection.get(
        limit=limit,
        include=["documents", "embeddings", "metadatas"]
    )

