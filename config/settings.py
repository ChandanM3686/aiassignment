"""
Configuration settings for the Math Mentor application.
Loads settings from environment variables with sensible defaults.
Uses Gemini for LLM and embeddings with quota protection.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)


@dataclass
class Settings:
    """Application configuration settings."""
    
    # Gemini API Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")
    
    # Whisper Settings
    whisper_model: str = os.getenv("WHISPER_MODEL", "base")
    
    # Confidence Thresholds
    ocr_confidence_threshold: float = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.6"))
    asr_confidence_threshold: float = float(os.getenv("ASR_CONFIDENCE_THRESHOLD", "0.7"))
    verifier_confidence_threshold: float = float(os.getenv("VERIFIER_CONFIDENCE_THRESHOLD", "0.7"))
    
    # RAG Settings (reduced to save quota)
    rag_top_k: int = int(os.getenv("RAG_TOP_K", "2"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Memory Settings
    memory_similarity_threshold: float = float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.8"))
    max_similar_problems: int = int(os.getenv("MAX_SIMILAR_PROBLEMS", "2"))
    
    # Paths
    knowledge_base_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
    data_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    chroma_db_path: str = os.path.join(data_path, "chroma_db")
    memory_db_path: str = os.path.join(data_path, "memory.db")
    embedding_cache_path: str = os.path.join(data_path, "embedding_cache.json")
    
    def __post_init__(self):
        """Validate required settings and create directories."""
        # Create data directories if they don't exist
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.chroma_db_path, exist_ok=True)
        
        # Validate API key
        if not self.gemini_api_key:
            print("Warning: GEMINI_API_KEY not set. Some features may not work.")
    
    def validate(self) -> bool:
        """Validate that all required settings are present."""
        if not self.gemini_api_key:
            return False
        return True


# Global settings instance (no caching, reads fresh values)
_settings = None

def get_settings() -> Settings:
    """Get settings instance."""
    global _settings
    if _settings is None:
        load_dotenv(override=True)  # Force reload
        _settings = Settings()
    return _settings
