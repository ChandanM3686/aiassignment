"""
RAG Retriever for the Math Mentor application.
Handles retrieval of relevant context for math problems.
Gracefully handles missing knowledge base.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from config.settings import get_settings


@dataclass
class RetrievedContext:
    """Represents a retrieved context with metadata."""
    content: str
    source: str
    category: str
    topic: str
    relevance_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "source": self.source,
            "category": self.category,
            "topic": self.topic,
            "relevance_score": self.relevance_score
        }


class Retriever:
    """RAG retriever with source attribution. Works without knowledge base if not built."""
    
    def __init__(self, vector_store=None):
        """Initialize the retriever.
        
        Args:
            vector_store: Optional VectorStore instance.
        """
        self.settings = get_settings()
        self.top_k = self.settings.rag_top_k
        self._vector_store = vector_store
        self._initialized = False
        self._available = False
    
    def _lazy_init(self):
        """Lazily initialize vector store only when needed."""
        if self._initialized:
            return
        
        self._initialized = True
        
        try:
            # Check if knowledge base exists first
            from .knowledge_base import is_knowledge_base_initialized
            
            if not is_knowledge_base_initialized():
                print("⚠️ Knowledge base not built - RAG disabled")
                self._available = False
                return
            
            # Only import and create vector store if KB exists
            from .vector_store import VectorStore
            self._vector_store = VectorStore()
            self._available = True
            print("✅ RAG retriever initialized")
            
        except Exception as e:
            print(f"⚠️ RAG initialization failed: {e}")
            self._available = False
    
    def retrieve(
        self,
        query: str,
        n_results: Optional[int] = None,
        category_filter: Optional[str] = None
    ) -> List[RetrievedContext]:
        """Retrieve relevant context for a query.
        
        Args:
            query: The search query.
            n_results: Optional number of results (default: top_k from settings).
            category_filter: Optional category to filter by.
            
        Returns:
            List of RetrievedContext objects (empty if KB not available).
        """
        self._lazy_init()
        
        if not self._available or self._vector_store is None:
            return []
        
        try:
            n = n_results or self.top_k
            
            # Build filter if category specified
            where_filter = None
            if category_filter:
                where_filter = {"category": category_filter}
            
            # Query the vector store
            results = self._vector_store.query(
                query_text=query,
                n_results=n,
                where=where_filter
            )
            
            # Convert to RetrievedContext objects
            contexts = []
            for i, doc in enumerate(results["documents"]):
                metadata = results["metadatas"][i] if results["metadatas"] else {}
                distance = results["distances"][i] if results["distances"] else 1.0
                
                # Convert distance to similarity score (lower distance = higher similarity)
                relevance_score = 1.0 / (1.0 + distance)
                
                context = RetrievedContext(
                    content=doc,
                    source=metadata.get("source", "unknown"),
                    category=metadata.get("category", "general"),
                    topic=metadata.get("topic", "unknown"),
                    relevance_score=round(relevance_score, 4)
                )
                contexts.append(context)
            
            return contexts
            
        except Exception as e:
            print(f"⚠️ Retrieval error: {e}")
            return []
    
    def retrieve_for_topic(
        self,
        query: str,
        topic: str
    ) -> List[RetrievedContext]:
        """Retrieve context filtered by topic.
        
        Args:
            query: The search query.
            topic: The topic to filter by (e.g., 'algebra', 'calculus').
            
        Returns:
            List of RetrievedContext objects.
        """
        # Map common topic names to categories
        topic_mapping = {
            "algebra": "algebra",
            "quadratic": "algebra",
            "polynomial": "algebra",
            "probability": "probability",
            "permutation": "probability",
            "combination": "probability",
            "calculus": "calculus",
            "derivative": "calculus",
            "integral": "calculus",
            "limit": "calculus",
            "matrix": "linear_algebra",
            "vector": "linear_algebra",
            "determinant": "linear_algebra",
        }
        
        category = topic_mapping.get(topic.lower(), None)
        return self.retrieve(query, category_filter=category)
    
    def retrieve_with_fallback(
        self,
        query: str,
        topic: Optional[str] = None
    ) -> List[RetrievedContext]:
        """Retrieve with fallback to general search if topic-filtered returns few results.
        
        Args:
            query: The search query.
            topic: Optional topic filter.
            
        Returns:
            List of RetrievedContext objects.
        """
        if topic:
            # Try topic-filtered search first
            results = self.retrieve_for_topic(query, topic)
            
            # If we got enough results, return them
            if len(results) >= 2:
                return results
            
            # Otherwise, supplement with general search
            general_results = self.retrieve(query)
            
            # Combine and deduplicate
            seen_sources = {r.source for r in results}
            for r in general_results:
                if r.source not in seen_sources:
                    results.append(r)
                    seen_sources.add(r.source)
            
            return results[:self.top_k]
        
        return self.retrieve(query)
    
    def format_context_for_prompt(
        self,
        contexts: List[RetrievedContext]
    ) -> str:
        """Format retrieved contexts for inclusion in LLM prompt.
        
        Args:
            contexts: List of RetrievedContext objects.
            
        Returns:
            Formatted string for prompt injection.
        """
        if not contexts:
            return "Note: Knowledge base not available. Solve using your training knowledge."
        
        formatted_parts = ["## Retrieved Knowledge Base Context:\n"]
        
        for i, ctx in enumerate(contexts, 1):
            formatted_parts.append(
                f"### Source {i}: {ctx.topic} ({ctx.category})\n"
                f"*Relevance: {ctx.relevance_score:.2%}*\n\n"
                f"{ctx.content}\n\n"
                f"---\n"
            )
        
        return "\n".join(formatted_parts)
    
    def get_sources_summary(
        self,
        contexts: List[RetrievedContext]
    ) -> List[Dict[str, Any]]:
        """Get a summary of sources used.
        
        Args:
            contexts: List of RetrievedContext objects.
            
        Returns:
            List of source summaries for UI display.
        """
        if not contexts:
            return [{"source": "AI Knowledge", "topic": "General", "category": "N/A", "relevance": "N/A", "preview": "Using AI's built-in knowledge (RAG not available)"}]
        
        return [
            {
                "source": ctx.source,
                "topic": ctx.topic,
                "category": ctx.category,
                "relevance": f"{ctx.relevance_score:.2%}",
                "preview": ctx.content[:150] + "..." if len(ctx.content) > 150 else ctx.content
            }
            for ctx in contexts
        ]
