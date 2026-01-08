import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import chromadb
from app.config.settings import settings
from app.services.embedding_service import generate_embedding
import re

def chunk_text(text: str):
    sections = re.split(r"\n\d+\.\s+", text)
    chunks = []
    for section in sections:
        cleaned = section.strip()
        if cleaned:
            chunks.append(cleaned)
    return chunks

def seed_test_data():
    print(f"🔧 Using Chroma at: {settings.CHROMA_PERSIST_DIR}")
    
    # Initializing client directly
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    collection = client.get_or_create_collection(name="company_policies")
    
    print(f"Initial collection count: {collection.count()}")
    
    test_documents = [
        {
            "id": "safety_policy_001",
            "text": "1. All employees must complete safety training within their first 30 days."
        }
    ]
    
    for doc in test_documents:
        print(f"\nAdding document: {doc['id']}")
        
        # Simple test - just one chunk
        try:
            embedding = generate_embedding(doc['text'])
            print(f" Generated embedding ({len(embedding)} dimensions)")
            
            collection.add(
                documents=[doc['text']],
                embeddings=[embedding],
                ids=[doc['id']],
                metadatas=[{"doc_id": doc['id'], "source": "seed"}]
            )
            
            print(f" Added to collection")
            print(f"New count: {collection.count()}")
            
        except Exception as e:
            print(f" Error adding document: {e}")
    
    # Verifying all data
    print(f"\nFinal verification:")
    all_data = collection.get()
    print(f"Total documents: {len(all_data['ids'])}")
    print(f"Document IDs: {all_data['ids']}")

if __name__ == "__main__":
    seed_test_data()