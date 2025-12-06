"""
Image Processing Module for Multi-Modal Firewall
Handles OCR, QR code detection, and image sanitization
"""

import base64
import io
from typing import Dict, List, Optional, Tuple
from PIL import Image
import easyocr
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np


class ImageProcessor:
    """
    Processes images to extract text, detect QR codes, and sanitize content
    """
    
    def __init__(self, ocr_language: str = 'en'):
        """
        Initialize image processor
        
        Args:
            ocr_language: Language for OCR (default: 'en')
        """
        self.ocr_reader = easyocr.Reader([ocr_language], gpu=False)
        self.processed_images = {}  # Cache for processed images
    
    def is_image(self, content: str) -> bool:
        """
        Check if content is an image (base64, file path, or URL)
        
        Args:
            content: Content to check
            
        Returns:
            True if content appears to be an image
        """
        # Check for base64 image
        if content.startswith('data:image/') or content.startswith('/9j/'):
            return True
        
        # Check for image file extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        content_lower = content.lower().strip()
        if any(content_lower.endswith(ext) for ext in image_extensions):
            return True
        
        # Check for image URLs
        if content.startswith('http') and any(ext in content_lower for ext in image_extensions):
            return True
        
        return False
    
    def load_image(self, image_input: str) -> Optional[Image.Image]:
        """
        Load image from various formats (base64, file path, URL)
        
        Args:
            image_input: Image as base64 string, file path, or URL
            
        Returns:
            PIL Image object or None if loading fails
        """
        try:
            # Try base64
            if image_input.startswith('data:image/'):
                # data:image/png;base64,iVBORw0KG...
                header, encoded = image_input.split(',', 1)
                image_data = base64.b64decode(encoded)
                return Image.open(io.BytesIO(image_data))
            elif image_input.startswith('/9j/'):
                # Raw base64 JPEG
                image_data = base64.b64decode(image_input)
                return Image.open(io.BytesIO(image_data))
            
            # Try file path
            try:
                return Image.open(image_input)
            except:
                pass
            
            # Try URL (would need requests library)
            # For now, skip URL loading - can be added later
            
            return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def extract_text_ocr(self, image: Image.Image) -> List[Dict[str, any]]:
        """
        Extract text from image using OCR
        
        Args:
            image: PIL Image object
            
        Returns:
            List of dictionaries with 'text', 'confidence', 'bbox' for each detected text
        """
        try:
            # Convert PIL to numpy array for EasyOCR
            img_array = np.array(image)
            
            # Run OCR
            results = self.ocr_reader.readtext(img_array)
            
            extracted_texts = []
            for (bbox, text, confidence) in results:
                extracted_texts.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
            
            return extracted_texts
        except Exception as e:
            print(f"OCR extraction error: {e}")
            return []
    
    def detect_qr_codes(self, image: Image.Image) -> List[Dict[str, str]]:
        """
        Detect and decode QR codes in image
        
        Args:
            image: PIL Image object
            
        Returns:
            List of dictionaries with 'data' and 'type' for each QR code
        """
        try:
            # Convert PIL to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale if needed
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Decode QR codes
            decoded_objects = pyzbar.decode(gray)
            
            qr_results = []
            for obj in decoded_objects:
                qr_results.append({
                    'data': obj.data.decode('utf-8'),
                    'type': obj.type,
                    'rect': obj.rect
                })
            
            return qr_results
        except Exception as e:
            print(f"QR code detection error: {e}")
            return []
    
    def process_image(self, image_input: str) -> Dict[str, any]:
        """
        Complete image processing pipeline
        
        Args:
            image_input: Image as base64, file path, or URL
            
        Returns:
            Dictionary with:
            - 'success': bool
            - 'text_extracted': str (combined OCR text)
            - 'ocr_results': List of OCR detections
            - 'qr_codes': List of QR code data
            - 'image': PIL Image object
            - 'warnings': List of warnings
        """
        result = {
            'success': False,
            'text_extracted': '',
            'ocr_results': [],
            'qr_codes': [],
            'image': None,
            'warnings': []
        }
        
        # Load image
        image = self.load_image(image_input)
        if image is None:
            result['warnings'].append("Failed to load image")
            return result
        
        result['image'] = image
        result['success'] = True
        
        # Extract text via OCR
        ocr_results = self.extract_text_ocr(image)
        result['ocr_results'] = ocr_results
        
        # Combine all OCR text
        all_text = ' '.join([item['text'] for item in ocr_results])
        result['text_extracted'] = all_text
        
        # Detect QR codes
        qr_codes = self.detect_qr_codes(image)
        result['qr_codes'] = qr_codes
        
        # Add QR code data to extracted text
        if qr_codes:
            qr_text = ' '.join([qr['data'] for qr in qr_codes])
            result['text_extracted'] += ' ' + qr_text
            result['warnings'].append(f"Detected {len(qr_codes)} QR code(s)")
        
        return result
    
    def sanitize_image(self, image: Image.Image, sensitive_regions: List[Tuple[int, int, int, int]]) -> Image.Image:
        """
        Blur or redact sensitive regions in image
        
        Args:
            image: PIL Image object
            sensitive_regions: List of (x1, y1, x2, y2) bounding boxes to redact
            
        Returns:
            Sanitized PIL Image
        """
        try:
            img_array = np.array(image)
            
            for x1, y1, x2, y2 in sensitive_regions:
                # Blur the region
                region = img_array[y1:y2, x1:x2]
                blurred = cv2.GaussianBlur(region, (51, 51), 0)
                img_array[y1:y2, x1:x2] = blurred
            
            return Image.fromarray(img_array)
        except Exception as e:
            print(f"Image sanitization error: {e}")
            return image



