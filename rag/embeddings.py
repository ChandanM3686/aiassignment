"""
Gemini Embeddings wrapper with aggressive caching and rate limiting.
Minimizes API calls to protect quota.
"""

import os
import json
import time
import hashlib
import google.generativeai as genai
from typing import List, Optional, Dict
from config.settings import get_settings

# Global cache and rate limiter
_embedding_cache: Dict[str, List[float]] = {}
_cache_loaded = False
_last_api_call = 0
_MIN_DELAY_SECONDS = 0.5  # Minimum delay between API calls


def _get_cache_path():
    """Get the cache file path."""
    settings = get_settings()
    return settings.embedding_cache_path


def _load_cache():
    """Load embedding cache from file."""
    global _embedding_cache, _cache_loaded
    if _cache_loaded:
        return
    
    cache_path = _get_cache_path()
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                _embedding_cache = json.load(f)
            print(f"Loaded {len(_embedding_cache)} cached embeddings")
        except Exception as e:
            print(f"Could not load cache: {e}")
            _embedding_cache = {}
    _cache_loaded = True


def _save_cache():
    """Save embedding cache to file."""
    try:
        cache_path = _get_cache_path()
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, 'w') as f:
            json.dump(_embedding_cache, f)
    except Exception as e:
        print(f"Could not save cache: {e}")


def _get_cache_key(text: str) -> str:
    """Generate a cache key for text."""
    return hashlib.md5(text.strip().lower().encode()).hexdigest()


def _rate_limit():
    """Enforce rate limiting between API calls."""
    global _last_api_call
    elapsed = time.time() - _last_api_call
    if elapsed < _MIN_DELAY_SECONDS:
        time.sleep(_MIN_DELAY_SECONDS - elapsed)
    _last_api_call = time.time()


class GeminiEmbeddings:
    """Wrapper for Gemini embedding model with caching."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini embeddings client."""
        _load_cache()
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model = settings.embedding_model
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text with caching."""
        # Check cache first
        cache_key = _get_cache_key(text)
        if cache_key in _embedding_cache:
            return _embedding_cache[cache_key]
        
        try:
            _rate_limit()  # Enforce rate limiting
            
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            embedding = result['embedding']
            
            # Cache the result
            _embedding_cache[cache_key] = embedding
            _save_cache()
            
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Return empty list on error
            return []
    
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        # Check cache first
        cache_key = _get_cache_key(query)
        if cache_key in _embedding_cache:
            return _embedding_cache[cache_key]
        
        try:
            _rate_limit()
            
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            embedding = result['embedding']
            
            # Cache the result
            _embedding_cache[cache_key] = embedding
            _save_cache()
            
            return embedding
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents with caching."""
        embeddings = []
        new_embeddings = 0
        
        for doc in documents:
            cache_key = _get_cache_key(doc)
            if cache_key in _embedding_cache:
                embeddings.append(_embedding_cache[cache_key])
            else:
                embedding = self.embed_text(doc)
                embeddings.append(embedding)
                if embedding:
                    new_embeddings += 1
        
        if new_embeddings > 0:
            print(f"Generated {new_embeddings} new embeddings (cached: {len(documents) - new_embeddings})")
        
        return embeddings
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Make the class callable for ChromaDB compatibility."""
        return self.embed_documents(texts)


class GeminiEmbeddingFunction:
    """ChromaDB-compatible embedding function using Gemini with caching."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key."""
        self.embedder = GeminiEmbeddings(api_key)
        self._name = "gemini-embedding-cached"
    
    def name(self) -> str:
        """Return the name of this embedding function (required by ChromaDB 1.3+)."""
        return self._name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for ChromaDB."""
        return self.embedder.embed_documents(input)
