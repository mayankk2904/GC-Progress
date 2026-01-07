from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Vector CRUD with Ollama")

app.include_router(router)
