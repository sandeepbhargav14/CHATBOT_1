from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class AppConfig(BaseModel):
    # App settings
    APP_NAME: str = "Website-Based AI Chatbot"
    CHUNK_SIZE: int = Field(default=500, description="Text chunk size")
    CHUNK_OVERLAP: int = Field(default=50, description="Chunk overlap size")

    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Vector DB
    VECTOR_DB_PATH: str = "data/vector_db/"

    # LLM
    LLM_MODEL_NAME: Optional[str] = "openai/gpt-oss-120b:free"


config = AppConfig()
