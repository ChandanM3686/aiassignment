"""
Vector Store implementation using ChromaDB.
Handles storage and retrieval of embedded documents.
Includes rate limiting for quota protection.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import os
import time

from config.settings import get_settings
from .embeddings import GeminiEmbeddingFunction


class VectorStore:
    """ChromaDB-based vector store for math knowledge."""
    
    def __init__(self, collection_name: str = "math_knowledge"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection.
        """
        self.settings = get_settings()
        self.collection_name = collection_name
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(
            path=self.settings.chroma_db_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create embedding function
        self.embedding_function = GeminiEmbeddingFunction(self.settings.gemini_api_key)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "JEE Math Knowledge Base"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """Add documents to the vector store with rate limiting.
        
        Args:
            documents: List of document texts.
            metadatas: Optional list of metadata dicts.
            ids: Optional list of unique IDs.
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in documents]
        
        # Add in very small batches with delays to avoid quota limits
        # Gemini free tier: 1500 requests/day, 15 requests/minute
        batch_size = 5  # Very small batches
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        for i in range(0, len(documents), batch_size):
            batch_num = i // batch_size + 1
            batch_docs = documents[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]
            
            print(f"  Processing batch {batch_num}/{total_batches} ({len(batch_docs)} docs)...")
            
            try:
                self.collection.add(
                    documents=batch_docs,
                    metadatas=batch_meta,
                    ids=batch_ids
                )
            except Exception as e:
                print(f"  Warning: Error in batch {batch_num}: {e}")
                # Continue with other batches
            
            # Rate limiting: wait between batches if not the last one
            if i + batch_size < len(documents):
                time.sleep(2)  # 2 second delay between batches
    
    def query(
        self,
        query_text: str,
        n_results: int = 2,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query the vector store for similar documents.
        
        Args:
            query_text: The search query.
            n_results: Number of results to return.
            where: Optional filter conditions.
            
        Returns:
            Dict containing documents, metadatas, distances, and ids.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "ids": results["ids"][0] if results["ids"] else []
        }
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(self.collection_name)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection.
        
        Returns:
            Dict with collection statistics.
        """
        return {
            "name": self.collection_name,
            "count": self.collection.count(),
        }
    
    def document_exists(self, doc_id: str) -> bool:
        """Check if a document exists in the collection.
        
        Args:
            doc_id: The document ID to check.
            
        Returns:
            True if document exists, False otherwise.
        """
        try:
            result = self.collection.get(ids=[doc_id])
            return len(result["ids"]) > 0
        except Exception:
            return False
