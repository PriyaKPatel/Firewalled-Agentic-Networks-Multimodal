"""
Setup script for Multimodal Firewall package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multimodal-firewall",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Multimodal extension for Firewalled Agentic Networks - Adds image, QR code, and OCR support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Firewalled-Agentic-Networks-Multimodal",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.9",
    install_requires=[
        "easyocr>=1.7.0",
        "pyzbar>=0.1.9",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "llm-guard>=0.3.0",
    ],
    extras_require={
        "gpu": ["torch>=2.0.0", "torchvision>=0.15.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
    keywords=[
        "llm",
        "security",
        "firewall",
        "multimodal",
        "ocr",
        "qr-code",
        "prompt-injection",
        "agentic-networks",
    ],
)

