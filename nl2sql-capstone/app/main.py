# app/main.py - Add test endpoint
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text  # Import text
from typing import List

from app import schemas, crud, models
from app.database import engine, get_db
from app.gemini_service import gemini_service

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Natural Language to SQL API",
    description="Convert natural language questions to SQL queries using Gemini AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Natural Language to SQL API",
        "endpoints": {
            "/": "This documentation",
            "/students/": "Get all students",
            "/students/create": "Create new student (POST)",
            "/query/": "Convert natural language to SQL and execute (POST)",
            "/test-sql/": "Test SQL query execution (POST)",
            "/health": "Health check",
            "/count": "Get student count directly"
        }
    }

@app.get("/students/", response_model=List[schemas.StudentResponse])
def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.post("/students/create", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@app.post("/test-sql/")
def test_sql_query(query: str, db: Session = Depends(get_db)):
    """
    Direct SQL query testing endpoint
    """
    try:
        result = crud.execute_sql_query(db, query)
        return {
            "query": query,
            "result": result,
            "row_count": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/count")
def get_student_count(db: Session = Depends(get_db)):
    """
    Direct endpoint to get student count
    """
    try:
        result = db.execute(text("SELECT COUNT(*) FROM students"))
        count = result.scalar()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check
    """
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        
        # Check student count
        result = db.execute(text("SELECT COUNT(*) FROM students"))
        count = result.scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "student_count": count,
            "service": "NL-to-SQL API"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/", response_model=schemas.SQLResponse)
def natural_language_to_sql(query: schemas.NLQuery, db: Session = Depends(get_db)):
    """
    Convert natural language question to SQL, execute it, and return results
    """
    try:
        print(f"Processing question: {query.question}")
        
        # Step 1: Generate SQL from natural language
        sql_query = gemini_service.generate_sql(query.question)
        print(f"Generated SQL: {sql_query}")
        
        # Step 2: Execute the SQL query
        result = crud.execute_sql_query(db, sql_query)
        print(f"Query result: {result}")
        
        # Step 3: Generate explanation
        explanation = gemini_service.explain_query(sql_query, result)
        
        return {
            "sql_query": sql_query,
            "result": result,
            "explanation": explanation,
            "row_count": len(result)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error details: {str(e)}")  # Log error
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")