from fastapi import APIRouter
from app.models.schemas import DocumentCreate, QueryRequest
from app.services.vector_service import (
    add_document,
    query_documents,
    update_document,
    delete_document,
    get_all_documents
)

router = APIRouter()

@router.post("/vectors")
def create_vector(doc: DocumentCreate):
    add_document(doc.id, doc.text)
    return {"message": "Document added successfully"}

@router.post("/vectors/query")
def read_vectors(request: QueryRequest):
    results = query_documents(request.query)
    return results

@router.put("/vectors/{doc_id}")
def update_vector(doc_id: str, doc: DocumentCreate):
    update_document(doc_id, doc.text)
    return {"message": "Document updated"}

@router.delete("/vectors/{doc_id}")
def delete_vector(doc_id: str):
    delete_document(doc_id)
    return {"message": "Document deleted"}

@router.get("/vectors")
def list_vectors(limit: int = 10):
    return get_all_documents(limit)

