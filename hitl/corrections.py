"""
Correction Handler - Manages user corrections for learning.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Correction:
    """Represents a user correction."""
    original_text: str
    corrected_text: str
    correction_type: str  # 'ocr', 'asr', 'solution', 'other'
    timestamp: datetime
    problem_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "corrected_text": self.corrected_text,
            "correction_type": self.correction_type,
            "timestamp": self.timestamp.isoformat(),
            "problem_id": self.problem_id
        }


class CorrectionHandler:
    """Handles storage and application of user corrections."""
    
    def __init__(self):
        """Initialize the correction handler."""
        self.corrections: List[Correction] = []
        self.correction_patterns: Dict[str, str] = {}
    
    def record_correction(
        self,
        original: str,
        corrected: str,
        correction_type: str,
        problem_id: str
    ) -> Correction:
        """Record a user correction.
        
        Args:
            original: Original text.
            corrected: Corrected text by user.
            correction_type: Type of correction.
            problem_id: ID of the problem.
            
        Returns:
            The recorded Correction.
        """
        correction = Correction(
            original_text=original,
            corrected_text=corrected,
            correction_type=correction_type,
            timestamp=datetime.now(),
            problem_id=problem_id
        )
        
        self.corrections.append(correction)
        
        # Learn pattern if it's a simple substitution
        if len(original) < 50 and len(corrected) < 50:
            self._learn_pattern(original, corrected, correction_type)
        
        return correction
    
    def _learn_pattern(self, original: str, corrected: str, correction_type: str) -> None:
        """Learn a correction pattern.
        
        Args:
            original: Original text.
            corrected: Corrected text.
            correction_type: Type of correction.
        """
        key = f"{correction_type}:{original.lower()}"
        
        # Only store if we've seen this pattern before or it's a direct correction
        if key in self.correction_patterns:
            # Update if we have a new correction
            existing = self.correction_patterns[key]
            if existing != corrected:
                # Could implement voting or recency-based selection
                self.correction_patterns[key] = corrected
        else:
            self.correction_patterns[key] = corrected
    
    def apply_known_corrections(self, text: str, correction_type: str) -> str:
        """Apply known corrections to text.
        
        Args:
            text: Text to correct.
            correction_type: Type of correction.
            
        Returns:
            Text with known corrections applied.
        """
        result = text
        
        # Apply exact matches first
        for original, corrected in self.correction_patterns.items():
            if original.startswith(f"{correction_type}:"):
                pattern = original.split(":", 1)[1]
                if pattern in result.lower():
                    # Case-insensitive replacement
                    import re
                    result = re.sub(
                        re.escape(pattern),
                        corrected,
                        result,
                        flags=re.IGNORECASE
                    )
        
        return result
    
    def get_corrections_for_type(self, correction_type: str) -> List[Correction]:
        """Get all corrections of a specific type.
        
        Args:
            correction_type: Type to filter by.
            
        Returns:
            List of matching corrections.
        """
        return [c for c in self.corrections if c.correction_type == correction_type]
    
    def get_correction_stats(self) -> Dict[str, Any]:
        """Get statistics about corrections.
        
        Returns:
            Dict with correction statistics.
        """
        from collections import Counter
        
        type_counts = Counter(c.correction_type for c in self.corrections)
        
        return {
            "total_corrections": len(self.corrections),
            "by_type": dict(type_counts),
            "learned_patterns": len(self.correction_patterns)
        }
    
    def export_corrections(self) -> List[Dict]:
        """Export all corrections.
        
        Returns:
            List of correction dicts.
        """
        return [c.to_dict() for c in self.corrections]
    
    def import_corrections(self, corrections: List[Dict]) -> None:
        """Import corrections from export.
        
        Args:
            corrections: List of correction dicts.
        """
        for c in corrections:
            correction = Correction(
                original_text=c["original_text"],
                corrected_text=c["corrected_text"],
                correction_type=c["correction_type"],
                timestamp=datetime.fromisoformat(c["timestamp"]),
                problem_id=c["problem_id"]
            )
            self.corrections.append(correction)
            self._learn_pattern(
                c["original_text"],
                c["corrected_text"],
                c["correction_type"]
            )
