"""
Configuration settings for the Math Mentor application.
Loads settings from environment variables or Streamlit secrets.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Try to load .env file (for local development)
load_dotenv(override=True)


def get_secret(key: str, default: str = "") -> str:
    """Get secret from Streamlit secrets or environment variable."""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    
    # Fall back to environment variable (for local development)
    return os.getenv(key, default)


@dataclass
class Settings:
    """Application configuration settings."""
    
    # Gemini API Configuration
    gemini_api_key: str = ""
    gemini_model: str = ""
    embedding_model: str = ""
    
    # Whisper Settings
    whisper_model: str = ""
    
    # Confidence Thresholds
    ocr_confidence_threshold: float = 0.6
    asr_confidence_threshold: float = 0.7
    verifier_confidence_threshold: float = 0.7
    
    # RAG Settings
    rag_top_k: int = 2
    chunk_size: int = 800
    chunk_overlap: int = 50
    
    # Memory Settings
    memory_similarity_threshold: float = 0.8
    max_similar_problems: int = 2
    
    # Paths
    knowledge_base_path: str = ""
    data_path: str = ""
    chroma_db_path: str = ""
    memory_db_path: str = ""
    embedding_cache_path: str = ""
    
    def __post_init__(self):
        """Load settings from secrets/env and create directories."""
        # Load from secrets or environment
        self.gemini_api_key = get_secret("GEMINI_API_KEY", "")
        self.gemini_model = get_secret("GEMINI_MODEL", "gemini-2.0-flash")
        self.embedding_model = get_secret("EMBEDDING_MODEL", "models/text-embedding-004")
        self.whisper_model = get_secret("WHISPER_MODEL", "base")
        
        self.ocr_confidence_threshold = float(get_secret("OCR_CONFIDENCE_THRESHOLD", "0.6"))
        self.asr_confidence_threshold = float(get_secret("ASR_CONFIDENCE_THRESHOLD", "0.7"))
        self.verifier_confidence_threshold = float(get_secret("VERIFIER_CONFIDENCE_THRESHOLD", "0.7"))
        
        self.rag_top_k = int(get_secret("RAG_TOP_K", "2"))
        self.chunk_size = int(get_secret("CHUNK_SIZE", "800"))
        self.chunk_overlap = int(get_secret("CHUNK_OVERLAP", "50"))
        
        self.memory_similarity_threshold = float(get_secret("MEMORY_SIMILARITY_THRESHOLD", "0.8"))
        self.max_similar_problems = int(get_secret("MAX_SIMILAR_PROBLEMS", "2"))
        
        # Set paths
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.knowledge_base_path = os.path.join(base_dir, "knowledge_base")
        self.data_path = os.path.join(base_dir, "data")
        self.chroma_db_path = os.path.join(self.data_path, "chroma_db")
        self.memory_db_path = os.path.join(self.data_path, "memory.db")
        self.embedding_cache_path = os.path.join(self.data_path, "embedding_cache.json")
        
        # Create data directories if they don't exist
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.chroma_db_path, exist_ok=True)
        
        # Validate API key
        if not self.gemini_api_key:
            print("Warning: GEMINI_API_KEY not set!")
    
    def validate(self) -> bool:
        """Validate that all required settings are present."""
        return bool(self.gemini_api_key)


# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
