"""
Image Handler for OCR processing.
Extracts text from math problem images with confidence scoring.
"""

import io
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from PIL import Image
import numpy as np

from config.settings import get_settings


@dataclass
class OCRResult:
    """Result from OCR processing."""
    text: str
    confidence: float
    needs_review: bool
    raw_results: list
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "needs_review": self.needs_review
        }


class ImageHandler:
    """Handles image input and OCR for math problems."""
    
    def __init__(self):
        """Initialize the image handler."""
        self.settings = get_settings()
        self.confidence_threshold = self.settings.ocr_confidence_threshold
        self._reader = None
    
    @property
    def reader(self):
        """Lazy load EasyOCR reader."""
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(['en'], gpu=False)
        return self._reader
    
    def process_image(self, image_data: bytes) -> OCRResult:
        """Process an image and extract text using OCR.
        
        Args:
            image_data: Raw image bytes.
            
        Returns:
            OCRResult with extracted text and confidence.
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array for EasyOCR
            image_array = np.array(image)
            
            # Perform OCR
            results = self.reader.readtext(image_array)
            
            # Extract text and calculate confidence
            extracted_text, avg_confidence = self._process_ocr_results(results)
            
            # Determine if human review is needed
            needs_review = avg_confidence < self.confidence_threshold
            
            return OCRResult(
                text=extracted_text,
                confidence=avg_confidence,
                needs_review=needs_review,
                raw_results=results
            )
            
        except Exception as e:
            print(f"OCR Error: {e}")
            return OCRResult(
                text="",
                confidence=0.0,
                needs_review=True,
                raw_results=[]
            )
    
    def process_image_file(self, file_path: str) -> OCRResult:
        """Process an image file.
        
        Args:
            file_path: Path to the image file.
            
        Returns:
            OCRResult with extracted text and confidence.
        """
        with open(file_path, 'rb') as f:
            image_data = f.read()
        return self.process_image(image_data)
    
    def _process_ocr_results(self, results: list) -> Tuple[str, float]:
        """Process raw OCR results into text and confidence.
        
        Args:
            results: Raw OCR results from EasyOCR.
            
        Returns:
            Tuple of (extracted_text, average_confidence).
        """
        if not results:
            return "", 0.0
        
        lines = []
        confidences = []
        
        # Sort results by vertical position (top to bottom)
        sorted_results = sorted(results, key=lambda x: x[0][0][1])
        
        for detection in sorted_results:
            bbox, text, confidence = detection
            lines.append(text)
            confidences.append(confidence)
        
        # Join lines into text
        extracted_text = ' '.join(lines)
        
        # Clean up common OCR errors for math
        extracted_text = self._clean_math_text(extracted_text)
        
        # Calculate average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return extracted_text, avg_confidence
    
    def _clean_math_text(self, text: str) -> str:
        """Clean OCR text for common math notation errors.
        
        Args:
            text: Raw OCR text.
            
        Returns:
            Cleaned text with math corrections.
        """
        # Common OCR corrections for math symbols
        replacements = {
            'xX': 'x',
            '×': '*',
            '÷': '/',
            '²': '^2',
            '³': '^3',
            '√': 'sqrt',
            'π': 'pi',
            '∞': 'infinity',
            '≠': '!=',
            '≤': '<=',
            '≥': '>=',
            '∈': 'in',
            '∑': 'sum',
            '∏': 'product',
            '∫': 'integral',
            '∂': 'd',  # partial derivative
            'Δ': 'delta',
            'θ': 'theta',
            'α': 'alpha',
            'β': 'beta',
            'γ': 'gamma',
            'λ': 'lambda',
            'μ': 'mu',
            'σ': 'sigma',
            'ω': 'omega',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Fix common OCR mistakes
        text = text.replace('O', '0').replace('o', '0') if 'equation' not in text.lower() else text
        text = text.replace('l', '1') if text.count('l') == 1 else text
        
        return text.strip()
    
    def preprocess_image(self, image_data: bytes) -> bytes:
        """Preprocess image for better OCR accuracy.
        
        Args:
            image_data: Raw image bytes.
            
        Returns:
            Preprocessed image bytes.
        """
        from PIL import ImageEnhance, ImageFilter
        
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Sharpen
        image = image.filter(ImageFilter.SHARPEN)
        
        # Convert back to RGB
        image = image.convert('RGB')
        
        # Save to bytes
        output = io.BytesIO()
        image.save(output, format='PNG')
        return output.getvalue()
