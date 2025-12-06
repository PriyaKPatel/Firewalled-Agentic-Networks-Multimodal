# Changelog

All notable changes to the Multimodal Firewall extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial release of Multimodal Firewall extension
- OCR text extraction using EasyOCR
- QR code detection and decoding using pyzbar
- LLM-Guard integration for security scanning
  - PromptInjection scanner
  - PII (Personally Identifiable Information) scanner
  - Toxicity scanner
  - Secrets scanner
- Regex-based malicious pattern detection
- Image sanitization (blur/redact sensitive regions)
- Auto-detection of content type (image vs text)
- Support for multiple image formats (PNG, JPEG, GIF, BMP, WebP)
- Base64 image support
- Comprehensive logging and scan history
- Demo script with example attacks
- Integration with existing Input Firewall
- Full documentation and README

### Security Improvements
- Multi-layer defense against image-based attacks
- Hidden text detection in images
- Malicious QR code blocking
- Risk score aggregation from multiple scanners

### Dependencies
- EasyOCR >= 1.7.0
- pyzbar >= 0.1.9
- opencv-python >= 4.8.0
- Pillow >= 10.0.0
- llm-guard >= 0.3.0

## [Unreleased]

### Planned Features
- PDF text extraction
- Video frame analysis
- Audio transcription and scanning
- Custom malicious pattern training
- Performance optimization with caching
- GPU acceleration for OCR
- Multi-language OCR support

---

## How to Update

```bash
# Update to latest version
pip install --upgrade multimodal-firewall

# Or update from source
git pull origin main
pip install -r requirements.txt
```

