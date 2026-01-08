from pydantic import BaseModel

class DocumentCreate(BaseModel):
    id: str
    text: str

class QueryRequest(BaseModel):
    query: str
