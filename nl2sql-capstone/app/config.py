from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    class Config:
        env_file = ".env"

settings = Settings()