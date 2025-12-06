# 📦 GitHub Repository Setup Guide

This guide explains how to create your GitHub repository with the Multimodal Firewall extension.

---

## Step 1: Create New GitHub Repository

1. Go to [GitHub](https://github.com) and login
2. Click **"+"** → **"New repository"**
3. Fill in details:
   - **Repository name**: `Firewalled-Agentic-Networks-Multimodal`
   - **Description**: `Extended version of Microsoft's Firewalled Agentic Networks with Multimodal Firewall support for images, QR codes, and OCR-based security scanning`
   - **Visibility**: Public (recommended for academic projects)
   - **Initialize**: Leave unchecked (we'll push existing code)
4. Click **"Create repository"**

---

## Step 2: Prepare Local Repository

```bash
# Navigate to project directory
cd /Users/priya/Projects/Firewalled-Agentic-Networks

# Rename README_NEW.md to README.md (backup original first)
mv README.md README_ORIGINAL.md
mv README_NEW.md README.md

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Multimodal Firewall extension for Firewalled Agentic Networks"
```

---

## Step 3: Push to GitHub

```bash
# Add remote origin (replace with your repo URL)
git remote add origin https://github.com/yourusername/Firewalled-Agentic-Networks-Multimodal.git

# Push to main branch
git branch -M main
git push -u origin main
```

---

## Step 4: Add Repository Topics (Optional)

On GitHub, click **"About"** → **"Add topics"**:
- `llm`
- `security`
- `firewall`
- `multimodal`
- `ocr`
- `prompt-injection`
- `agentic-networks`
- `llm-guard`
- `python`

---

## Step 5: Create Releases (Optional)

1. Go to **"Releases"** → **"Create a new release"**
2. Tag: `v1.0.0`
3. Title: `Multimodal Firewall v1.0.0`
4. Description: 
```
Initial release of Multimodal Firewall extension.

Features:
- OCR text extraction from images (EasyOCR)
- QR code detection and decoding (pyzbar)
- LLM-Guard integration for security scanning
- Multi-layer defense against image-based attacks
```

---

## 📁 Final Repository Structure

```
Firewalled-Agentic-Networks-Multimodal/
├── README.md                    # Main README (new)
├── README_ORIGINAL.md           # Original paper README
├── LICENSE                      # MIT License
├── config.yaml                  # Configuration
├── main.py                      # Main script
├── requirements.txt             # Dependencies
├── GITHUB_SETUP_GUIDE.md        # This file
│
├── multimodal_firewall/         # 🆕 YOUR EXTENSION
│   ├── __init__.py
│   ├── image_processor.py
│   ├── multimodal_filter.py
│   ├── demo.py
│   ├── requirements.txt
│   ├── setup.py
│   ├── README.md
│   ├── LICENSE
│   ├── CONTRIBUTING.md
│   ├── CHANGELOG.md
│   ├── .gitignore
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_multimodal.py
│   └── examples/
│       ├── __init__.py
│       └── example_usage.py
│
├── assistant/                   # Original
├── external_agent/              # Original (modified)
├── user_environment/            # Original
├── judge/                       # Original
├── mitigation_guidelines/       # Original
├── resources/                   # Original
└── all_outputs_with_judge/      # Original
```

---

## ✅ Checklist Before Publishing

- [ ] Replace `[Your Name]` with your actual name in LICENSE files
- [ ] Replace `yourusername` with your GitHub username in URLs
- [ ] Replace `your.email@example.com` with your email
- [ ] Test all code works: `python main.py`
- [ ] Test multimodal demo: `python multimodal_firewall/demo.py`
- [ ] Run tests: `pytest multimodal_firewall/tests/`
- [ ] Review README for accuracy
- [ ] Remove any sensitive data from config files

---

## 📝 Commit Messages Template

```bash
# Initial commit
git commit -m "Initial commit: Multimodal Firewall extension"

# Feature commits
git commit -m "Add: OCR text extraction with EasyOCR"
git commit -m "Add: QR code detection with pyzbar"
git commit -m "Add: LLM-Guard integration for security scanning"
git commit -m "Add: Demo script and examples"
git commit -m "Add: Unit tests for multimodal filter"
git commit -m "Add: Documentation and README files"

# Bug fixes
git commit -m "Fix: Handle base64 encoded images"
git commit -m "Fix: Improve error handling in OCR"

# Documentation
git commit -m "Docs: Update README with usage examples"
git commit -m "Docs: Add CONTRIBUTING guidelines"
```

---

## 🎯 Repository URL Format

Your repository will be at:
```
https://github.com/yourusername/Firewalled-Agentic-Networks-Multimodal
```

---

## 📧 Questions?

If you have issues setting up the repository, check:
1. Git is installed: `git --version`
2. GitHub CLI (optional): `gh auth login`
3. SSH keys are configured (for SSH URLs)

---

**Good luck with your project! 🚀**

