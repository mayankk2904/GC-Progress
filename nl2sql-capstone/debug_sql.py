# debug_sql.py
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()

# Test Gemini SQL generation
try:
    from app.gemini_service import gemini_service
    print("✅ Gemini service imported")
    
    # Test questions
    test_questions = [
        "How many students are there?",
        "Show all students in Data Science class",
        "What is the average marks?",
        "List students sorted by marks",
        "Find students with marks above 80"
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"Question: {question}")
        try:
            sql = gemini_service.generate_sql(question)
            print(f"Generated SQL: {sql}")
        except Exception as e:
            print(f"Error: {e}")
            
except ImportError as e:
    print(f"Import error: {e}")
    print("\nChecking files...")
    
    # List app directory
    app_dir = Path(__file__).parent / "app"
    if app_dir.exists():
        print(f"App directory: {app_dir}")
        for file in app_dir.iterdir():
            print(f"  - {file.name}")