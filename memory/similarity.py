"""
Similarity Search - Find similar previously solved problems.
"""

from typing import List, Optional, Tuple
import numpy as np

from .memory_store import MemoryStore, ProblemMemory
from rag.embeddings import GeminiEmbeddings
from config.settings import get_settings


class SimilaritySearch:
    """Search for similar previously solved problems."""
    
    def __init__(self, memory_store: MemoryStore = None):
        """Initialize similarity search.
        
        Args:
            memory_store: Optional MemoryStore instance.
        """
        self.settings = get_settings()
        self.memory_store = memory_store or MemoryStore()
        self.embeddings = GeminiEmbeddings()
        self.similarity_threshold = self.settings.memory_similarity_threshold
        self.max_results = self.settings.max_similar_problems
    
    def find_similar(
        self,
        query: str,
        topic: str = None,
        only_correct: bool = True
    ) -> List[Tuple[ProblemMemory, float]]:
        """Find similar previously solved problems.
        
        Args:
            query: Problem text to search for.
            topic: Optional topic filter.
            only_correct: Only return user-verified correct solutions.
            
        Returns:
            List of (ProblemMemory, similarity_score) tuples.
        """
        # Get query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        if not query_embedding:
            return []
        
        # Get candidate problems from memory
        if only_correct:
            candidates = self.memory_store.get_correct_solutions(limit=100)
        elif topic:
            candidates = self.memory_store.get_problems_by_topic(topic, limit=100)
        else:
            # Get recent problems (this should be paginated in production)
            candidates = self._get_all_problems(limit=100)
        
        # Filter to those with embeddings
        candidates_with_embeddings = [
            (p, p.embedding) for p in candidates if p.embedding
        ]
        
        if not candidates_with_embeddings:
            return []
        
        # Calculate similarities
        similarities = []
        for problem, embedding in candidates_with_embeddings:
            similarity = self._cosine_similarity(query_embedding, embedding)
            if similarity >= self.similarity_threshold:
                similarities.append((problem, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top results
        return similarities[:self.max_results]
    
    def _get_all_problems(self, limit: int = 100) -> List[ProblemMemory]:
        """Get all problems from memory (for searching).
        
        Args:
            limit: Max problems to retrieve.
            
        Returns:
            List of ProblemMemory.
        """
        # This is a simplified implementation
        # In production, would need pagination and caching
        conn = self.memory_store._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM problem_memory 
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self.memory_store._row_to_memory(row) for row in rows]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector.
            vec2: Second vector.
            
        Returns:
            Cosine similarity (0 to 1).
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        a = np.array(vec1)
        b = np.array(vec2)
        
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return float(dot_product / (norm_a * norm_b))
    
    def get_similar_solutions_context(
        self,
        query: str,
        topic: str = None
    ) -> str:
        """Get context string from similar solutions.
        
        Args:
            query: Problem text.
            topic: Optional topic filter.
            
        Returns:
            Formatted context string.
        """
        similar = self.find_similar(query, topic)
        
        if not similar:
            return ""
        
        lines = ["## Similar Previously Solved Problems:\n"]
        
        for i, (problem, similarity) in enumerate(similar, 1):
            lines.append(f"### Similar Problem {i} (Similarity: {similarity:.2%})")
            lines.append(f"**Question:** {problem.parsed_question[:200]}...")
            lines.append(f"**Answer:** {problem.final_answer}")
            lines.append(f"**Topic:** {problem.topic}/{problem.subtopic}")
            lines.append("")
        
        return "\n".join(lines)
    
    def add_embedding_to_problem(
        self,
        problem_id: str,
        text: str
    ) -> None:
        """Add embedding to an existing problem.
        
        Args:
            problem_id: Problem ID.
            text: Text to embed.
        """
        embedding = self.embeddings.embed_text(text)
        
        if embedding:
            conn = self.memory_store._get_connection()
            cursor = conn.cursor()
            
            import json
            cursor.execute("""
                UPDATE problem_memory 
                SET embedding = ?
                WHERE id = ?
            """, (json.dumps(embedding), problem_id))
            
            conn.commit()
            conn.close()
