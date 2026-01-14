import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
try:
    from app.database import SessionLocal, engine
    from app import models, schemas
    from app.crud import create_student
    print("✅ Successfully imported modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nChecking project structure...")
    
    # List files to debug
    current_dir = Path(__file__).parent
    print(f"Current directory: {current_dir}")
    if (current_dir / "app").exists():
        print("App folder exists")
        print("Files in app folder:")
        for file in (current_dir / "app").iterdir():
            print(f"  - {file.name}")
    sys.exit(1)


def seed_database():
    # Create tables first
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Sample data
        students_data = [
            {"name": "Krish", "class_name": "Data Science", "section": "A", "marks": 90},
            {"name": "Sudhanshu", "class_name": "Data Science", "section": "B", "marks": 100},
            {"name": "Darius", "class_name": "Data Science", "section": "A", "marks": 86},
            {"name": "Vikash", "class_name": "DEVOPS", "section": "A", "marks": 50},
            {"name": "Dipesh", "class_name": "DEVOPS", "section": "A", "marks": 35},
            {"name": "Amit", "class_name": "Machine Learning", "section": "C", "marks": 95},
            {"name": "Priya", "class_name": "Machine Learning", "section": "B", "marks": 88},
            {"name": "Raj", "class_name": "Web Development", "section": "A", "marks": 75},
            {"name": "Sneha", "class_name": "Web Development", "section": "C", "marks": 92},
            {"name": "Rohan", "class_name": "Data Science", "section": "B", "marks": 78}
        ]
        
        print(f"Seeding {len(students_data)} students...")
        
        # Add students to database
        for i, student_data in enumerate(students_data, 1):
            student = schemas.StudentCreate(**student_data)
            db_student = create_student(db, student)
            print(f"  {i}. Added {db_student.name} - {db_student.class_name}")
        
        db.commit()
        print("\n✅ Database seeded successfully!")
        print(f"✅ Added {len(students_data)} students to the database.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeding...")
    seed_database()