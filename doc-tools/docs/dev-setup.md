# Development Setup Guide

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher (3.13+ recommended)
- **Memory**: Minimum 4GB RAM (8GB recommended for large documentation sets)
- **Disk Space**: At least 2GB free space
- **Operating System**: Windows, macOS, or Linux

### Required Software
- Git for version control
- Python pip package manager
- Text editor or IDE (VS Code, PyCharm recommended)
- Terminal/Command Prompt access

## Installation Steps

### 1. Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/yourusername/DocScraper.git
cd DocScraper

# Or clone via SSH
git clone git@github.com:yourusername/DocScraper.git
cd DocScraper
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify activation (should show venv path)
which python
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (required for web scraping)
playwright install chromium

# Optional: Install development dependencies
pip install pytest black mypy pylint
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your configuration (see `.env.example` below):

```bash
# OpenAI API Configuration (Optional - for LLM features)
OPENAI_API_KEY=sk-your-api-key-here

# Scraping Configuration
MAX_CONCURRENT_REQUESTS=5
RATE_LIMIT_DELAY=1.0
USER_AGENT=DocScraper/1.0
TIMEOUT_MS=30000
CACHE_MODE=bypass

# Post-Processing Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_CHUNK_SIZE=1500
MIN_CHUNK_SIZE=500

# Output Configuration
DEFAULT_OUTPUT_DIR=scraped_docs
DEFAULT_PROCESSED_DIR=processed_docs

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=docscraper.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# GUI Configuration
GUI_THEME=default
GUI_WIDTH=800
GUI_HEIGHT=600

# Advanced Features
USE_PROXY=false
PROXY_URL=
VERIFY_SSL=true
FOLLOW_REDIRECTS=true
MAX_REDIRECTS=5
```

### 5. Verify Installation

```bash
# Test basic import
python -c "from DocScraper import DocumentationScraper; print('✓ DocScraper imported successfully')"

# Test Playwright installation
python -c "from playwright.async_api import async_playwright; print('✓ Playwright ready')"

# Test crawl4ai installation
python -c "from crawl4ai import AsyncWebCrawler; print('✓ Crawl4ai ready')"

# Run basic scraping test
python test_stop.py

# Check GUI components
python -c "import tkinter; print('✓ Tkinter GUI ready')"
```

## Project Structure

```
DocScraper/
├── .env                      # Environment variables (create this)
├── .env.example             # Example environment configuration
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
│
├── docs/                   # Documentation (you are here)
│   ├── overview.md
│   ├── architecture.md
│   ├── api.md
│   ├── data-model.md
│   ├── dev-setup.md       # This file
│   ├── testing.md
│   ├── security.md
│   ├── code-map.md
│   └── decisions/
│       └── 0001-architecture-baseline.md
│
├── DocScraper.py          # Main scraping module
├── SimpleDocScraper.py    # Simplified scraper
├── DocScraperGUI.py       # Scraper GUI
├── DocPostProcessor.py    # Post-processing module
├── DocPostProcessorGUI.py # Post-processor GUI
│
├── process_docs_example.py      # Usage examples
├── process_multi_folder_example.py
├── test_stop.py                 # Basic test script
│
├── scraped_docs/          # Default scraping output (gitignored)
├── processed_docs/        # Default processing output (gitignored)
├── Documentation/         # Sample scraped documentation
└── venv/                 # Virtual environment (gitignored)
```

## Development Workflow

### 1. Running the Scraper

#### Command Line
```bash
# Basic scraping
python DocScraper.py https://docs.example.com

# With custom output directory
python DocScraper.py https://docs.example.com my_docs

# With page limit
python DocScraper.py https://docs.example.com my_docs 100

# Simple scraper (sequential)
python SimpleDocScraper.py https://docs.example.com
```

#### GUI Interface
```bash
# Launch scraper GUI
python DocScraperGUI.py
```

### 2. Running the Post-Processor

#### Command Line
```bash
# Basic processing
python DocPostProcessor.py scraped_docs processed_docs

# With LLM classification
python DocPostProcessor.py scraped_docs processed_docs --use-llm

# Process multiple folders
python process_multi_folder_example.py
```

#### GUI Interface
```bash
# Launch post-processor GUI
python DocPostProcessorGUI.py
```

### 3. Development Commands

```bash
# Format code with Black
black *.py

# Type checking with mypy
mypy DocScraper.py

# Lint with pylint
pylint DocScraper.py

# Run tests
pytest tests/

# Generate test coverage
pytest --cov=. tests/
```

## IDE Configuration

### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "venv": true
    }
}
```

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Scraper CLI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/DocScraper.py",
            "args": ["https://docs.example.com"],
            "console": "integratedTerminal"
        },
        {
            "name": "Scraper GUI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/DocScraperGUI.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Post-Processor CLI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/DocPostProcessor.py",
            "args": ["scraped_docs", "processed_docs"],
            "console": "integratedTerminal"
        }
    ]
}
```

### PyCharm

1. Open project in PyCharm
2. Configure Python Interpreter:
   - File → Settings → Project → Python Interpreter
   - Select `venv/bin/python` from project directory
3. Mark directories:
   - Right-click `docs` → Mark Directory as → Sources Root
4. Configure run configurations:
   - Run → Edit Configurations
   - Add Python configurations for each main script

## Common Issues and Solutions

### Issue: ImportError for packages

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Playwright browsers not installed

**Solution:**
```bash
# Install Playwright browsers
playwright install chromium

# Or install all browsers
playwright install
```

### Issue: OpenAI API key not found

**Solution:**
```bash
# Check .env file exists and contains key
cat .env | grep OPENAI_API_KEY

# Ensure .env is in project root
ls -la | grep .env

# Load environment in Python
from dotenv import load_dotenv
load_dotenv()
```

### Issue: Tkinter not available (Linux)

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (should be included)
# Windows (should be included)
```

### Issue: Permission denied errors

**Solution:**
```bash
# Ensure output directories are writable
chmod 755 scraped_docs processed_docs

# Or run with user permissions
python DocScraper.py --output-dir ~/Documents/scraped_docs
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM features | None | No (for LLM features) |
| `MAX_CONCURRENT_REQUESTS` | Maximum parallel requests | 5 | No |
| `RATE_LIMIT_DELAY` | Delay between requests (seconds) | 1.0 | No |
| `CHUNK_SIZE` | Target chunk size in tokens | 1000 | No |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 | No |
| `LOG_LEVEL` | Logging verbosity | INFO | No |
| `DEFAULT_OUTPUT_DIR` | Default scraping output | scraped_docs | No |
| `DEFAULT_PROCESSED_DIR` | Default processing output | processed_docs | No |

## Testing Your Setup

### Quick Smoke Test

```bash
# Create test script
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

async def test_setup():
    tests_passed = 0
    tests_failed = 0
    
    # Test imports
    try:
        from DocScraper import DocumentationScraper
        print("✓ DocScraper import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"✗ DocScraper import failed: {e}")
        tests_failed += 1
    
    try:
        from DocPostProcessor import DocumentPostProcessor
        print("✓ DocPostProcessor import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"✗ DocPostProcessor import failed: {e}")
        tests_failed += 1
    
    # Test environment
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        if os.getenv('OPENAI_API_KEY'):
            print("✓ OpenAI API key configured")
        else:
            print("! OpenAI API key not set (optional)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Environment setup failed: {e}")
        tests_failed += 1
    
    # Test GUI availability
    try:
        import tkinter
        print("✓ Tkinter GUI available")
        tests_passed += 1
    except ImportError:
        print("! Tkinter not available (GUI won't work)")
        tests_failed += 1
    
    print(f"\nResults: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0

if __name__ == "__main__":
    success = asyncio.run(test_setup())
    sys.exit(0 if success else 1)
EOF

# Run test
python test_setup.py
```

## Next Steps

1. **Run a test scrape**: Try scraping a small documentation site
2. **Process the results**: Run the post-processor on scraped content
3. **Explore the GUI**: Launch the GUI applications to understand the interface
4. **Read the API docs**: Check [api.md](./api.md) for integration options
5. **Set up testing**: See [testing.md](./testing.md) for test configuration