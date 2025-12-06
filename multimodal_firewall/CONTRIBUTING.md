# Contributing to Multimodal Firewall

Thank you for your interest in contributing to the Multimodal Firewall extension!

## How to Contribute

### Reporting Issues

1. Check if the issue already exists in GitHub Issues
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Add tests if applicable
5. Run tests: `pytest tests/`
6. Format code: `black .`
7. Commit with clear message: `git commit -m "Add: your feature description"`
8. Push to your fork: `git push origin feature/your-feature-name`
9. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing

- Add unit tests for new features
- Ensure all existing tests pass
- Test with different image types and attack scenarios

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Firewalled-Agentic-Networks-Multimodal.git
cd Firewalled-Agentic-Networks-Multimodal/multimodal_firewall

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## Areas for Contribution

- [ ] PDF text extraction
- [ ] Video frame analysis
- [ ] Audio transcription
- [ ] Custom malicious pattern training
- [ ] Performance optimization
- [ ] Additional LLM-Guard scanners
- [ ] Multi-language OCR support
- [ ] Documentation improvements

## Questions?

Open a GitHub issue or contact the maintainers.

Thank you for contributing! 🎉

