"""
Multimodal Firewall - Extension for Firewalled Agentic Networks

This module extends the paper's text-only Input Firewall to handle 
images, QR codes, and multimodal content.

Paper: "Firewalls to Secure Dynamic LLM Agentic Networks"
Original Repository: https://github.com/microsoft/Firewalled-Agentic-Networks
Paper Link: https://arxiv.org/abs/2502.01822

Features:
- OCR text extraction from images (EasyOCR)
- QR code detection and decoding (pyzbar)
- LLM-Guard security scanning (PromptInjection, PII, Toxicity, Secrets)
- Multi-layer defense against multimodal attacks
- Seamless integration with existing firewalls

Usage:
    from multimodal_firewall import MultimodalFilter

    # Initialize filter
    filter = MultimodalFilter(use_llm_guard=True)

    # Process content (text or image)
    result = filter.process_content("path/to/image.png", content_type='image')
    
    # Check if safe
    if result['is_safe']:
        print("Content is safe:", result['sanitized'])
    else:
        print("Content blocked:", result['warnings'])

Author: [Your Name]
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

from .image_processor import ImageProcessor
from .multimodal_filter import MultimodalFilter

__all__ = [
    "ImageProcessor",
    "MultimodalFilter",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
