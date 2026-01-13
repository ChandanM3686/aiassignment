"""
HITL Triggers - Conditions that trigger human-in-the-loop intervention.
"""

from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass


class TriggerType(Enum):
    """Types of HITL triggers."""
    OCR_LOW_CONFIDENCE = "ocr_low_confidence"
    ASR_LOW_CONFIDENCE = "asr_low_confidence"
    PARSER_AMBIGUITY = "parser_ambiguity"
    VERIFIER_UNCERTAINTY = "verifier_uncertainty"
    USER_REQUESTED = "user_requested"
    SOLUTION_ERROR = "solution_error"


@dataclass
class HITLTrigger:
    """Represents a HITL trigger event."""
    trigger_type: TriggerType
    reason: str
    confidence: float
    data: Dict[str, Any]
    requires_edit: bool  # True if user should edit content
    requires_approval: bool  # True if user should approve/reject
    suggested_action: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger_type": self.trigger_type.value,
            "reason": self.reason,
            "confidence": self.confidence,
            "data": self.data,
            "requires_edit": self.requires_edit,
            "requires_approval": self.requires_approval,
            "suggested_action": self.suggested_action
        }


class HITLTriggerManager:
    """Manages HITL trigger logic."""
    
    def __init__(
        self,
        ocr_threshold: float = 0.6,
        asr_threshold: float = 0.7,
        verifier_threshold: float = 0.7
    ):
        """Initialize with thresholds.
        
        Args:
            ocr_threshold: Confidence threshold for OCR.
            asr_threshold: Confidence threshold for ASR.
            verifier_threshold: Confidence threshold for verification.
        """
        self.ocr_threshold = ocr_threshold
        self.asr_threshold = asr_threshold
        self.verifier_threshold = verifier_threshold
    
    def check_ocr_trigger(
        self,
        confidence: float,
        extracted_text: str
    ) -> Optional[HITLTrigger]:
        """Check if OCR result triggers HITL.
        
        Args:
            confidence: OCR confidence score.
            extracted_text: Extracted text.
            
        Returns:
            HITLTrigger if triggered, None otherwise.
        """
        if confidence < self.ocr_threshold:
            return HITLTrigger(
                trigger_type=TriggerType.OCR_LOW_CONFIDENCE,
                reason=f"OCR confidence ({confidence:.2%}) is below threshold ({self.ocr_threshold:.2%})",
                confidence=confidence,
                data={"extracted_text": extracted_text},
                requires_edit=True,
                requires_approval=False,
                suggested_action="Please review and correct the extracted text if needed"
            )
        return None
    
    def check_asr_trigger(
        self,
        confidence: float,
        transcript: str
    ) -> Optional[HITLTrigger]:
        """Check if ASR result triggers HITL.
        
        Args:
            confidence: ASR confidence score.
            transcript: Transcribed text.
            
        Returns:
            HITLTrigger if triggered, None otherwise.
        """
        if confidence < self.asr_threshold:
            return HITLTrigger(
                trigger_type=TriggerType.ASR_LOW_CONFIDENCE,
                reason=f"Speech recognition confidence ({confidence:.2%}) is below threshold ({self.asr_threshold:.2%})",
                confidence=confidence,
                data={"transcript": transcript},
                requires_edit=True,
                requires_approval=False,
                suggested_action="Please review and correct the transcript if needed"
            )
        return None
    
    def check_parser_trigger(
        self,
        needs_clarification: bool,
        clarification_needed: str,
        confidence: float
    ) -> Optional[HITLTrigger]:
        """Check if parser result triggers HITL.
        
        Args:
            needs_clarification: Whether clarification is needed.
            clarification_needed: What needs clarification.
            confidence: Parser confidence.
            
        Returns:
            HITLTrigger if triggered, None otherwise.
        """
        if needs_clarification or confidence < 0.6:
            return HITLTrigger(
                trigger_type=TriggerType.PARSER_AMBIGUITY,
                reason=clarification_needed or "Problem statement is ambiguous",
                confidence=confidence,
                data={"clarification_needed": clarification_needed},
                requires_edit=True,
                requires_approval=False,
                suggested_action="Please clarify the problem statement"
            )
        return None
    
    def check_verifier_trigger(
        self,
        is_correct: bool,
        confidence: float,
        errors: list
    ) -> Optional[HITLTrigger]:
        """Check if verification result triggers HITL.
        
        Args:
            is_correct: Whether solution is verified correct.
            confidence: Verifier confidence.
            errors: List of errors found.
            
        Returns:
            HITLTrigger if triggered, None otherwise.
        """
        if not is_correct or confidence < self.verifier_threshold or errors:
            error_summary = "; ".join(errors[:3]) if errors else "Uncertain about correctness"
            return HITLTrigger(
                trigger_type=TriggerType.VERIFIER_UNCERTAINTY,
                reason=f"Solution verification uncertain: {error_summary}",
                confidence=confidence,
                data={"is_correct": is_correct, "errors": errors},
                requires_edit=False,
                requires_approval=True,
                suggested_action="Please review the solution and verify correctness"
            )
        return None
    
    def create_user_trigger(self) -> HITLTrigger:
        """Create a user-requested HITL trigger.
        
        Returns:
            HITLTrigger for user request.
        """
        return HITLTrigger(
            trigger_type=TriggerType.USER_REQUESTED,
            reason="User requested manual review",
            confidence=0.0,
            data={},
            requires_edit=True,
            requires_approval=True,
            suggested_action="Please review and make any necessary corrections"
        )
