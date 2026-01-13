"""
Audio Handler for speech-to-text processing.
Converts spoken math questions to text using Whisper.
"""

import io
import os
import tempfile
from typing import Dict, Any, Optional
from dataclasses import dataclass

from config.settings import get_settings


@dataclass
class ASRResult:
    """Result from audio speech recognition."""
    transcript: str
    confidence: float
    needs_review: bool
    language: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "confidence": self.confidence,
            "needs_review": self.needs_review,
            "language": self.language
        }


class AudioHandler:
    """Handles audio input and speech-to-text conversion."""
    
    def __init__(self):
        """Initialize the audio handler."""
        self.settings = get_settings()
        self.confidence_threshold = self.settings.asr_confidence_threshold
        self.model_name = self.settings.whisper_model
        self._model = None
    
    @property
    def model(self):
        """Lazy load Whisper model."""
        if self._model is None:
            import whisper
            self._model = whisper.load_model(self.model_name)
        return self._model
    
    def process_audio(self, audio_data: bytes, file_extension: str = "wav") -> ASRResult:
        """Process audio data and convert to text.
        
        Args:
            audio_data: Raw audio bytes.
            file_extension: Audio file extension (e.g., 'wav', 'mp3').
            
        Returns:
            ASRResult with transcript and confidence.
        """
        try:
            # Save audio to temporary file (Whisper requires file path)
            with tempfile.NamedTemporaryFile(
                suffix=f".{file_extension}",
                delete=False
            ) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            try:
                # Transcribe audio
                result = self.model.transcribe(temp_path)
                
                # Extract transcript
                transcript = result.get("text", "").strip()
                
                # Process math phrases
                transcript = self._convert_math_phrases(transcript)
                
                # Calculate confidence from segments
                confidence = self._calculate_confidence(result)
                
                # Determine if review is needed
                needs_review = confidence < self.confidence_threshold
                
                return ASRResult(
                    transcript=transcript,
                    confidence=confidence,
                    needs_review=needs_review,
                    language=result.get("language", "en")
                )
                
            finally:
                # Clean up temp file
                os.unlink(temp_path)
                
        except Exception as e:
            print(f"ASR Error: {e}")
            return ASRResult(
                transcript="",
                confidence=0.0,
                needs_review=True,
                language="en"
            )
    
    def process_audio_file(self, file_path: str) -> ASRResult:
        """Process an audio file.
        
        Args:
            file_path: Path to the audio file.
            
        Returns:
            ASRResult with transcript and confidence.
        """
        with open(file_path, 'rb') as f:
            audio_data = f.read()
        
        extension = file_path.split('.')[-1]
        return self.process_audio(audio_data, extension)
    
    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate overall confidence from Whisper result.
        
        Args:
            result: Whisper transcription result.
            
        Returns:
            Average confidence score.
        """
        segments = result.get("segments", [])
        
        if not segments:
            return 0.5  # Default confidence for empty results
        
        # Whisper provides no_speech_prob for segments
        # Lower no_speech_prob = more confident it contains speech
        # We also consider avg_logprob
        
        confidences = []
        for segment in segments:
            no_speech = segment.get("no_speech_prob", 0.5)
            avg_logprob = segment.get("avg_logprob", -1.0)
            
            # Convert log prob to probability (approximate)
            # avg_logprob is typically between -1 and 0
            prob_score = max(0, 1 + avg_logprob)
            
            # Combine with speech detection
            segment_conf = prob_score * (1 - no_speech)
            confidences.append(segment_conf)
        
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    def _convert_math_phrases(self, text: str) -> str:
        """Convert spoken math phrases to mathematical notation.
        
        Args:
            text: Raw transcript.
            
        Returns:
            Text with math phrases converted.
        """
        # Math phrase conversions
        conversions = {
            # Basic operations
            "plus": "+",
            "minus": "-",
            "times": "*",
            "multiplied by": "*",
            "divided by": "/",
            "over": "/",
            
            # Powers
            "squared": "^2",
            "cubed": "^3",
            "to the power of": "^",
            "raised to": "^",
            "to the": "^",
            
            # Roots
            "square root of": "sqrt(",
            "cube root of": "cbrt(",
            "root of": "sqrt(",
            
            # Comparisons
            "equals": "=",
            "is equal to": "=",
            "greater than": ">",
            "less than": "<",
            "greater than or equal to": ">=",
            "less than or equal to": "<=",
            "not equal to": "!=",
            
            # Functions
            "sine of": "sin(",
            "cosine of": "cos(",
            "tangent of": "tan(",
            "log of": "log(",
            "natural log of": "ln(",
            "absolute value of": "abs(",
            
            # Constants
            "pi": "π",
            "infinity": "∞",
            "e to the": "e^",
            
            # Variables
            "x squared": "x^2",
            "x cubed": "x^3",
            "y squared": "y^2",
            "y cubed": "y^3",
            
            # Common phrases
            "find x": "find x",
            "solve for x": "solve for x",
            "what is the value of": "find",
            "calculate": "calculate",
            "evaluate": "evaluate",
            "simplify": "simplify",
            "differentiate": "d/dx",
            "integrate": "∫",
            "the derivative of": "d/dx",
            "the integral of": "∫",
            "limit as": "lim",
            "approaches": "→",
        }
        
        result = text.lower()
        
        # Apply conversions (longest phrases first to avoid partial matches)
        sorted_conversions = sorted(conversions.keys(), key=len, reverse=True)
        for phrase in sorted_conversions:
            result = result.replace(phrase, conversions[phrase])
        
        # Handle "x to the n" patterns
        import re
        result = re.sub(r'(\w)\s*to the\s*(\d+)', r'\1^\2', result)
        
        # Clean up spacing
        result = ' '.join(result.split())
        
        # Add closing parentheses for functions
        for func in ['sqrt(', 'cbrt(', 'sin(', 'cos(', 'tan(', 'log(', 'ln(', 'abs(']:
            if func in result and result.count(func) > result.count(')'):
                result += ')' * (result.count(func) - result.count(')'))
        
        return result.strip()
