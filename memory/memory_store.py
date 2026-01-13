"""
Memory Store - Persistent storage for problem-solution pairs.
"""

import sqlite3
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from config.settings import get_settings


@dataclass
class ProblemMemory:
    """Memory entry for a solved problem."""
    id: str
    timestamp: datetime
    input_type: str
    raw_input: str
    parsed_question: str
    topic: str
    subtopic: str
    retrieved_context: str
    solution: str
    explanation: str
    final_answer: str
    verifier_confidence: float
    user_feedback: str  # 'correct', 'incorrect', or ''
    user_comment: str
    embedding: Optional[List[float]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "input_type": self.input_type,
            "raw_input": self.raw_input,
            "parsed_question": self.parsed_question,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "retrieved_context": self.retrieved_context,
            "solution": self.solution,
            "explanation": self.explanation,
            "final_answer": self.final_answer,
            "verifier_confidence": self.verifier_confidence,
            "user_feedback": self.user_feedback,
            "user_comment": self.user_comment
        }


class MemoryStore:
    """SQLite-based memory store for problem-solution pairs."""
    
    def __init__(self, db_path: str = None):
        """Initialize the memory store.
        
        Args:
            db_path: Path to SQLite database.
        """
        settings = get_settings()
        self.db_path = db_path or settings.memory_db_path
        self._ensure_tables()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _ensure_tables(self) -> None:
        """Create tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Problem memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS problem_memory (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                input_type TEXT,
                raw_input TEXT,
                parsed_question TEXT,
                topic TEXT,
                subtopic TEXT,
                retrieved_context TEXT,
                solution TEXT,
                explanation TEXT,
                final_answer TEXT,
                verifier_confidence REAL,
                user_feedback TEXT,
                user_comment TEXT,
                embedding BLOB
            )
        """)
        
        # Corrections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS corrections (
                id TEXT PRIMARY KEY,
                original_text TEXT,
                corrected_text TEXT,
                correction_type TEXT,
                timestamp TEXT,
                frequency INTEGER DEFAULT 1
            )
        """)
        
        # Indices for faster retrieval
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_topic 
            ON problem_memory(topic, subtopic)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback 
            ON problem_memory(user_feedback)
        """)
        
        conn.commit()
        conn.close()
    
    def save_problem(self, memory: ProblemMemory) -> None:
        """Save a problem to memory.
        
        Args:
            memory: ProblemMemory to save.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        embedding_blob = json.dumps(memory.embedding) if memory.embedding else None
        
        cursor.execute("""
            INSERT OR REPLACE INTO problem_memory
            (id, timestamp, input_type, raw_input, parsed_question, topic, subtopic,
             retrieved_context, solution, explanation, final_answer, 
             verifier_confidence, user_feedback, user_comment, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory.id,
            memory.timestamp.isoformat(),
            memory.input_type,
            memory.raw_input,
            memory.parsed_question,
            memory.topic,
            memory.subtopic,
            memory.retrieved_context,
            memory.solution,
            memory.explanation,
            memory.final_answer,
            memory.verifier_confidence,
            memory.user_feedback,
            memory.user_comment,
            embedding_blob
        ))
        
        conn.commit()
        conn.close()
    
    def get_problem(self, problem_id: str) -> Optional[ProblemMemory]:
        """Get a problem by ID.
        
        Args:
            problem_id: Problem ID.
            
        Returns:
            ProblemMemory or None.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM problem_memory WHERE id = ?", (problem_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_memory(row)
        return None
    
    def get_problems_by_topic(
        self,
        topic: str,
        subtopic: str = None,
        limit: int = 10
    ) -> List[ProblemMemory]:
        """Get problems by topic.
        
        Args:
            topic: Main topic.
            subtopic: Optional subtopic.
            limit: Maximum results.
            
        Returns:
            List of ProblemMemory.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if subtopic:
            cursor.execute("""
                SELECT * FROM problem_memory 
                WHERE topic = ? AND subtopic = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (topic, subtopic, limit))
        else:
            cursor.execute("""
                SELECT * FROM problem_memory 
                WHERE topic = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (topic, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_memory(row) for row in rows]
    
    def get_correct_solutions(self, limit: int = 50) -> List[ProblemMemory]:
        """Get problems marked as correct by users.
        
        Args:
            limit: Maximum results.
            
        Returns:
            List of correct ProblemMemory.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM problem_memory 
            WHERE user_feedback = 'correct'
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_memory(row) for row in rows]
    
    def update_feedback(
        self,
        problem_id: str,
        feedback: str,
        comment: str = ""
    ) -> None:
        """Update user feedback for a problem.
        
        Args:
            problem_id: Problem ID.
            feedback: 'correct' or 'incorrect'.
            comment: Optional comment.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE problem_memory 
            SET user_feedback = ?, user_comment = ?
            WHERE id = ?
        """, (feedback, comment, problem_id))
        
        conn.commit()
        conn.close()
    
    def save_correction(
        self,
        original: str,
        corrected: str,
        correction_type: str
    ) -> None:
        """Save a correction pattern.
        
        Args:
            original: Original text.
            corrected: Corrected text.
            correction_type: Type of correction.
        """
        import hashlib
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create ID from original text
        correction_id = hashlib.md5(
            f"{correction_type}:{original}".encode()
        ).hexdigest()
        
        # Try to update existing, or insert new
        cursor.execute("""
            INSERT INTO corrections (id, original_text, corrected_text, correction_type, timestamp, frequency)
            VALUES (?, ?, ?, ?, ?, 1)
            ON CONFLICT(id) DO UPDATE SET
                corrected_text = excluded.corrected_text,
                frequency = frequency + 1
        """, (
            correction_id,
            original,
            corrected,
            correction_type,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_corrections(self, correction_type: str = None) -> Dict[str, str]:
        """Get learned correction patterns.
        
        Args:
            correction_type: Optional type filter.
            
        Returns:
            Dict mapping original -> corrected.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if correction_type:
            cursor.execute("""
                SELECT original_text, corrected_text 
                FROM corrections
                WHERE correction_type = ?
            """, (correction_type,))
        else:
            cursor.execute("SELECT original_text, corrected_text FROM corrections")
        
        rows = cursor.fetchall()
        conn.close()
        
        return {row["original_text"]: row["corrected_text"] for row in rows}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory store statistics.
        
        Returns:
            Dict with statistics.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Total problems
        cursor.execute("SELECT COUNT(*) as count FROM problem_memory")
        total = cursor.fetchone()["count"]
        
        # By feedback
        cursor.execute("""
            SELECT user_feedback, COUNT(*) as count 
            FROM problem_memory 
            GROUP BY user_feedback
        """)
        feedback_counts = {row["user_feedback"] or "pending": row["count"] 
                          for row in cursor.fetchall()}
        
        # By topic
        cursor.execute("""
            SELECT topic, COUNT(*) as count 
            FROM problem_memory 
            GROUP BY topic
        """)
        topic_counts = {row["topic"]: row["count"] for row in cursor.fetchall()}
        
        # Corrections
        cursor.execute("SELECT COUNT(*) as count FROM corrections")
        correction_count = cursor.fetchone()["count"]
        
        conn.close()
        
        return {
            "total_problems": total,
            "by_feedback": feedback_counts,
            "by_topic": topic_counts,
            "total_corrections": correction_count
        }
    
    def _row_to_memory(self, row: sqlite3.Row) -> ProblemMemory:
        """Convert database row to ProblemMemory."""
        embedding = None
        if row["embedding"]:
            embedding = json.loads(row["embedding"])
        
        return ProblemMemory(
            id=row["id"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            input_type=row["input_type"],
            raw_input=row["raw_input"],
            parsed_question=row["parsed_question"],
            topic=row["topic"],
            subtopic=row["subtopic"],
            retrieved_context=row["retrieved_context"],
            solution=row["solution"],
            explanation=row["explanation"],
            final_answer=row["final_answer"],
            verifier_confidence=row["verifier_confidence"],
            user_feedback=row["user_feedback"] or "",
            user_comment=row["user_comment"] or "",
            embedding=embedding
        )
    
    def test_connection(self) -> bool:
        """Test database connection.
        
        Returns:
            True if connection works.
        """
        try:
            conn = self._get_connection()
            conn.close()
            return True
        except Exception:
            return False
