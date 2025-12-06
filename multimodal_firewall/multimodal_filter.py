"""
Multi-Modal Filter - Main firewall for images + text
Integrates OCR, QR detection, and LLM-Guard scanning
"""

import json
import re
from typing import Dict, List, Optional, Tuple
try:
    from .image_processor import ImageProcessor
except ImportError:
    # Fallback for direct import
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from multimodal_firewall.image_processor import ImageProcessor

try:
    from llm_guard import scan_prompt, scan_output
    from llm_guard.input_scanners import (
        PromptInjection,
        Toxicity,
        Secrets,
    )
    from llm_guard.output_scanners import Sensitive, MaliciousURLs
    LLM_GUARD_AVAILABLE = True
    print("✅ LLM-Guard loaded successfully!")
except ImportError as e:
    LLM_GUARD_AVAILABLE = False
    print(f"⚠️ LLM-Guard not available: {e}")


class MultimodalFilter:
    """
    Multi-modal firewall that processes both text and images
    """
    
    def __init__(self, use_llm_guard: bool = True, ocr_language: str = 'en'):
        """
        Initialize multimodal filter
        
        Args:
            use_llm_guard: Whether to use LLM-Guard for text scanning
            ocr_language: Language for OCR
        """
        self.image_processor = ImageProcessor(ocr_language=ocr_language)
        self.use_llm_guard = use_llm_guard and LLM_GUARD_AVAILABLE
        
        # Initialize LLM-Guard scanners if available
        # Using comprehensive set of scanners for maximum security
        if self.use_llm_guard:
            self.input_scanners = [
                PromptInjection(),      # Detect prompt injection attacks
                Toxicity(),            # Detect toxic/harmful content
                Secrets(),             # Detect secrets (API keys, passwords, etc.)
            ]
            self.output_scanners = [
                Sensitive(),           # Detect sensitive information in outputs
                MaliciousURLs(),       # Detect malicious URLs
            ]
        else:
            self.input_scanners = []
            self.output_scanners = []
        
        # Malicious patterns to detect
        self.malicious_patterns = [
            r'ignore\s+(all\s+)?previous\s+instructions?',
            r'forget\s+(all\s+)?previous\s+instructions?',
            r'reveal\s+(user\s+)?(credit\s+card|password|ssn|social\s+security)',
            r'send\s+(email|message)\s+to\s+[^\s]+@[^\s]+',
            r'execute\s+(code|command|script)',
            r'bypass\s+(security|firewall|filter)',
        ]
        
        self.scan_history = []  # Log all scans
    
    def detect_malicious_text(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect malicious patterns in text using regex
        
        Args:
            text: Text to scan
            
        Returns:
            Tuple of (is_malicious, detected_patterns)
        """
        text_lower = text.lower()
        detected = []
        
        for pattern in self.malicious_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    def scan_with_llm_guard(self, text: str) -> Dict[str, any]:
        """
        Scan text using LLM-Guard
        
        Args:
            text: Text to scan
            
        Returns:
            Dictionary with scan results
        """
        if not self.use_llm_guard:
            return {
                'sanitized': text,
                'is_safe': True,
                'scans': {},
                'warnings': ['LLM-Guard not available']
            }
        
        try:
            # LLM-Guard returns (sanitized_text, scan_results_dict)
            sanitized, results = scan_prompt(self.input_scanners, text)
            
            # Aggregate risk scores and check for violations
            max_risk = 0.0
            is_valid = True
            detected_threats = []
            
            for scanner_name, result in results.items():
                # Check if scanner detected a threat
                if isinstance(result, dict):
                    # Some scanners return 'is_valid' boolean
                    if 'is_valid' in result and not result['is_valid']:
                        is_valid = False
                        detected_threats.append(scanner_name)
                    
                    # Some scanners return 'risk_score' (0.0 to 1.0)
                    if 'risk_score' in result:
                        max_risk = max(max_risk, result['risk_score'])
                        if result['risk_score'] > 0.7:  # High risk threshold
                            detected_threats.append(f"{scanner_name} (risk: {result['risk_score']:.2f})")
                
                # Some scanners return boolean directly
                elif isinstance(result, bool) and not result:
                    is_valid = False
                    detected_threats.append(scanner_name)
            
            # Determine if content is safe
            # Block if: invalid OR high risk score OR threats detected
            is_safe = is_valid and max_risk < 0.7 and len(detected_threats) == 0
            
            warnings = []
            if detected_threats:
                warnings.append(f"Threats detected: {', '.join(detected_threats)}")
            if max_risk > 0.5:
                warnings.append(f"High risk score: {max_risk:.2f}")
            
            return {
                'sanitized': sanitized,
                'is_safe': is_safe,
                'scans': results,
                'max_risk_score': max_risk,
                'detected_threats': detected_threats,
                'warnings': warnings
            }
        except Exception as e:
            return {
                'sanitized': text,
                'is_safe': True,
                'scans': {},
                'warnings': [f'LLM-Guard scan error: {e}']
            }
    
    def process_content(self, content: str, content_type: str = 'auto') -> Dict[str, any]:
        """
        Main processing function - handles both text and images
        
        Args:
            content: Content to process (text string or image)
            content_type: 'text', 'image', or 'auto' (auto-detect)
            
        Returns:
            Dictionary with:
            - 'success': bool
            - 'content_type': detected type
            - 'original': original content
            - 'sanitized': sanitized content
            - 'is_safe': bool
            - 'extracted_text': extracted text (if image)
            - 'warnings': List of warnings
            - 'scan_results': scan results
        """
        result = {
            'success': False,
            'content_type': 'unknown',
            'original': content,
            'sanitized': content,
            'is_safe': True,
            'extracted_text': '',
            'warnings': [],
            'scan_results': {}
        }
        
        # Auto-detect content type
        if content_type == 'auto':
            if self.image_processor.is_image(content):
                content_type = 'image'
            else:
                content_type = 'text'
        
        result['content_type'] = content_type
        
        # Process based on type
        if content_type == 'image':
            # Process image
            image_result = self.image_processor.process_image(content)
            
            if not image_result['success']:
                result['warnings'].extend(image_result['warnings'])
                result['sanitized'] = "[IMAGE PROCESSING FAILED]"
                result['is_safe'] = False
                return result
            
            # Extract text from image
            extracted_text = image_result['text_extracted']
            result['extracted_text'] = extracted_text
            
            # Scan extracted text
            if extracted_text:
                # Check for malicious patterns
                is_malicious, patterns = self.detect_malicious_text(extracted_text)
                
                # Scan with LLM-Guard
                scan_result = self.scan_with_llm_guard(extracted_text)
                
                result['scan_results'] = scan_result
                
                # Determine if safe
                if is_malicious or not scan_result['is_safe']:
                    result['is_safe'] = False
                    result['warnings'].append("Malicious content detected in image")
                    result['warnings'].append(f"Detected patterns: {patterns}")
                    result['sanitized'] = "[BLOCKED: Malicious content detected in image]"
                else:
                    # Create sanitized summary
                    result['sanitized'] = f"[IMAGE: {len(image_result['ocr_results'])} text regions, {len(image_result['qr_codes'])} QR codes. Extracted text: {extracted_text[:200]}...]"
            
            # Log QR codes
            if image_result['qr_codes']:
                qr_data = [qr['data'] for qr in image_result['qr_codes']]
                result['warnings'].append(f"QR codes detected: {qr_data}")
                
                # Scan QR code data
                for qr_data_item in qr_data:
                    is_malicious, _ = self.detect_malicious_text(qr_data_item)
                    if is_malicious:
                        result['is_safe'] = False
                        result['warnings'].append(f"Malicious QR code detected: {qr_data_item[:50]}")
                        result['sanitized'] = "[BLOCKED: Malicious QR code detected]"
            
            result['success'] = True
            
        else:  # content_type == 'text'
            # Process text directly
            is_malicious, patterns = self.detect_malicious_text(content)
            scan_result = self.scan_with_llm_guard(content)
            
            result['scan_results'] = scan_result
            result['extracted_text'] = content
            
            if is_malicious or not scan_result['is_safe']:
                result['is_safe'] = False
                result['warnings'].append("Malicious content detected")
                result['warnings'].append(f"Detected patterns: {patterns}")
                result['sanitized'] = scan_result.get('sanitized', "[BLOCKED: Malicious content]")
            else:
                result['sanitized'] = scan_result.get('sanitized', content)
            
            result['success'] = True
        
        # Log scan
        self.scan_history.append({
            'content_type': content_type,
            'is_safe': result['is_safe'],
            'warnings': result['warnings']
        })
        
        return result
    
    def get_scan_summary(self) -> Dict[str, any]:
        """
        Get summary of all scans performed
        
        Returns:
            Dictionary with scan statistics
        """
        total_scans = len(self.scan_history)
        blocked_scans = sum(1 for scan in self.scan_history if not scan['is_safe'])
        
        return {
            'total_scans': total_scans,
            'blocked_scans': blocked_scans,
            'allowed_scans': total_scans - blocked_scans,
            'block_rate': blocked_scans / total_scans if total_scans > 0 else 0.0
        }

