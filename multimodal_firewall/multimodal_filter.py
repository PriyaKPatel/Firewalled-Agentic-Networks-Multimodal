import re
from typing import Dict, List, Tuple

try:
    from .image_processor import ImageProcessor
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from multimodal_firewall.image_processor import ImageProcessor

try:
    from llm_guard import scan_prompt
    from llm_guard.input_scanners import PromptInjection, Toxicity, Secrets
    from llm_guard.output_scanners import Sensitive, MaliciousURLs
    LLM_GUARD_AVAILABLE = True
except ImportError:
    LLM_GUARD_AVAILABLE = False


class MultimodalFilter:
    
    def __init__(self, use_llm_guard: bool = True, ocr_language: str = 'en'):
        self.image_processor = ImageProcessor(ocr_language=ocr_language)
        self.use_llm_guard = use_llm_guard and LLM_GUARD_AVAILABLE
        
        if self.use_llm_guard:
            self.input_scanners = [
                PromptInjection(),
                Toxicity(),
                Secrets(),
            ]
            self.output_scanners = [
                Sensitive(),
                MaliciousURLs(),
            ]
        else:
            self.input_scanners = []
            self.output_scanners = []
        
        self.malicious_patterns = [
            r'ignore\s+(all\s+)?previous\s+instructions?',
            r'forget\s+(all\s+)?previous\s+instructions?',
            r'reveal\s+(user\s+)?(credit\s+card|password|ssn|social\s+security)',
            r'send\s+(email|message)\s+to\s+[^\s]+@[^\s]+',
            r'execute\s+(code|command|script)',
            r'bypass\s+(security|firewall|filter)',
        ]
        
        self.scan_history = []
    
    def detect_malicious_text(self, text: str) -> Tuple[bool, List[str]]:
        text_lower = text.lower()
        detected = []
        
        for pattern in self.malicious_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(pattern)
        
        return len(detected) > 0, detected
    
    def scan_with_llm_guard(self, text: str) -> Dict[str, any]:
        if not self.use_llm_guard:
            return {
                'sanitized': text,
                'is_safe': True,
                'scans': {},
                'warnings': ['LLM-Guard not available']
            }
        
        try:
            sanitized, results = scan_prompt(self.input_scanners, text)
            
            max_risk = 0.0
            is_valid = True
            detected_threats = []
            
            for scanner_name, result in results.items():
                if isinstance(result, dict):
                    if 'is_valid' in result and not result['is_valid']:
                        is_valid = False
                        detected_threats.append(scanner_name)
                    
                    if 'risk_score' in result:
                        max_risk = max(max_risk, result['risk_score'])
                        if result['risk_score'] > 0.7:
                            detected_threats.append(f"{scanner_name} (risk: {result['risk_score']:.2f})")
                
                elif isinstance(result, bool) and not result:
                    is_valid = False
                    detected_threats.append(scanner_name)
            
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
        
        if content_type == 'auto':
            content_type = 'image' if self.image_processor.is_image(content) else 'text'
        
        result['content_type'] = content_type
        
        if content_type == 'image':
            image_result = self.image_processor.process_image(content)
            
            if not image_result['success']:
                result['warnings'].extend(image_result['warnings'])
                result['sanitized'] = "[IMAGE PROCESSING FAILED]"
                result['is_safe'] = False
                return result
            
            extracted_text = image_result['text_extracted']
            result['extracted_text'] = extracted_text
            
            if extracted_text:
                is_malicious, patterns = self.detect_malicious_text(extracted_text)
                scan_result = self.scan_with_llm_guard(extracted_text)
                result['scan_results'] = scan_result
                
                if is_malicious or not scan_result['is_safe']:
                    result['is_safe'] = False
                    result['warnings'].append("Malicious content detected in image")
                    result['warnings'].append(f"Detected patterns: {patterns}")
                    result['sanitized'] = "[BLOCKED: Malicious content detected in image]"
                else:
                    result['sanitized'] = f"[IMAGE: {len(image_result['ocr_results'])} text regions, {len(image_result['qr_codes'])} QR codes. Extracted text: {extracted_text[:200]}...]"
            
            if image_result['qr_codes']:
                qr_data = [qr['data'] for qr in image_result['qr_codes']]
                result['warnings'].append(f"QR codes detected: {qr_data}")
                
                for qr_data_item in qr_data:
                    is_malicious, _ = self.detect_malicious_text(qr_data_item)
                    if is_malicious:
                        result['is_safe'] = False
                        result['warnings'].append(f"Malicious QR code detected: {qr_data_item[:50]}")
                        result['sanitized'] = "[BLOCKED: Malicious QR code detected]"
            
            result['success'] = True
            
        else:
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
        
        self.scan_history.append({
            'content_type': content_type,
            'is_safe': result['is_safe'],
            'warnings': result['warnings']
        })
        
        return result
    
    def get_scan_summary(self) -> Dict[str, any]:
        total_scans = len(self.scan_history)
        blocked_scans = sum(1 for scan in self.scan_history if not scan['is_safe'])
        
        return {
            'total_scans': total_scans,
            'blocked_scans': blocked_scans,
            'allowed_scans': total_scans - blocked_scans,
            'block_rate': blocked_scans / total_scans if total_scans > 0 else 0.0
        }

