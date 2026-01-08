import pandas as pd
import json
from app.db.chroma_client import collection

def export_vectors():
    data = collection.get(include=["documents", "metadatas", "embeddings"])

    print("IDs:", data["ids"])
    print("Count:", len(data["ids"]))


    rows = []
    for i in range(len(data["ids"])):
        rows.append({
            "id": data["ids"][i],
            "text": data["documents"][i],
            "metadata": data["metadatas"][i],
            "embedding_dim": len(data["embeddings"][i])
        })

    df = pd.DataFrame(rows)
    df.to_excel("chroma_vectors.xlsx", index=False)

    with open("chroma_vectors.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print("Vector dump created")

if __name__ == "__main__":
    export_vectors()
