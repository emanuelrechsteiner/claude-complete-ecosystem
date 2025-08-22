# Testing Documentation

## Testing Strategy

DocScraper employs a multi-layered testing approach to ensure reliability and quality:

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Measure speed and resource usage
5. **GUI Tests**: Validate user interface functionality

## Running Tests

### Quick Test Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_scraper.py

# Run specific test
pytest tests/test_scraper.py::test_url_validation

# Run with verbose output
pytest -v

# Run only marked tests
pytest -m "unit"
pytest -m "integration"
pytest -m "not slow"
```

### Test Coverage Goals

Current coverage targets:
- **Unit Tests**: 80% minimum
- **Integration Tests**: 60% minimum
- **Critical Path**: 95% minimum

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_scraper.py          # Scraper unit tests
├── test_post_processor.py   # Post-processor tests
├── test_cleaner.py          # Cleaner tests
├── test_structurer.py       # Structurer tests
├── test_sorter.py           # Sorter tests
├── test_integration.py      # Integration tests
├── test_gui.py              # GUI tests
├── test_performance.py      # Performance tests
├── fixtures/                # Test data
│   ├── sample_docs/
│   ├── expected_output/
│   └── mock_responses/
└── utils/                   # Test utilities
    ├── mock_server.py
    └── test_helpers.py
```

## Writing Tests

### Unit Test Example

```python
# tests/test_scraper.py
import pytest
from unittest.mock import Mock, patch
from DocScraper import DocumentationScraper

class TestDocumentationScraper:
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing."""
        return DocumentationScraper(output_dir="test_output")
    
    def test_url_validation_valid(self, scraper):
        """Test that valid URLs are accepted."""
        scraper.domain = "docs.example.com"
        
        valid_urls = [
            "https://docs.example.com/guide",
            "https://docs.example.com/api/endpoints",
            "https://docs.example.com/",
        ]
        
        for url in valid_urls:
            assert scraper._is_valid_doc_url(url) == True
    
    def test_url_validation_invalid(self, scraper):
        """Test that invalid URLs are rejected."""
        scraper.domain = "docs.example.com"
        
        invalid_urls = [
            "https://other.example.com/guide",  # Wrong domain
            "https://docs.example.com/file.pdf",  # PDF file
            "mailto:admin@example.com",  # Email link
            "javascript:void(0)",  # JavaScript
        ]
        
        for url in invalid_urls:
            assert scraper._is_valid_doc_url(url) == False
    
    @patch('DocScraper.AsyncWebCrawler')
    async def test_crawl_documentation(self, mock_crawler, scraper):
        """Test the main crawling function."""
        mock_response = Mock()
        mock_response.markdown = "# Test Page\nContent here"
        mock_response.url = "https://docs.example.com/test"
        
        mock_crawler.return_value.arun.return_value = mock_response
        
        result = await scraper.crawl_documentation(
            "https://docs.example.com",
            max_pages=1
        )
        
        assert result['total_pages'] == 1
        assert result['successful'] == 1
        assert result['failed'] == 0
```

### Integration Test Example

```python
# tests/test_integration.py
import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil

from DocScraper import DocumentationScraper
from DocPostProcessor import DocumentPostProcessor

class TestEndToEnd:
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        scraped = tempfile.mkdtemp(prefix="test_scraped_")
        processed = tempfile.mkdtemp(prefix="test_processed_")
        
        yield scraped, processed
        
        # Cleanup
        shutil.rmtree(scraped, ignore_errors=True)
        shutil.rmtree(processed, ignore_errors=True)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_scrape_and_process(self, temp_dirs):
        """Test complete scraping and processing workflow."""
        scraped_dir, processed_dir = temp_dirs
        
        # Step 1: Scrape documentation
        scraper = DocumentationScraper(output_dir=scraped_dir)
        scrape_result = await scraper.crawl_documentation(
            "https://docs.example.com",
            max_pages=5
        )
        
        assert scrape_result['successful'] > 0
        assert Path(scraped_dir).exists()
        assert len(list(Path(scraped_dir).glob("*.md"))) > 0
        
        # Step 2: Process scraped content
        processor = DocumentPostProcessor(
            input_dir=scraped_dir,
            output_dir=processed_dir
        )
        process_result = await processor.process_all_documents()
        
        assert process_result['total_documents'] > 0
        assert process_result['total_chunks'] > 0
        assert Path(processed_dir, "vector_db_index.json").exists()
```

### GUI Test Example

```python
# tests/test_gui.py
import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from DocScraperGUI import DocScraperGUI

class TestDocScraperGUI:
    
    @pytest.fixture
    def app(self):
        """Create GUI application for testing."""
        root = tk.Tk()
        app = DocScraperGUI(root)
        yield app
        root.destroy()
    
    def test_gui_initialization(self, app):
        """Test GUI initializes correctly."""
        assert app.root is not None
        assert app.url_entry is not None
        assert app.start_button is not None
        assert app.progress_bar is not None
    
    def test_url_validation_in_gui(self, app):
        """Test URL validation in GUI."""
        # Valid URL
        app.url_entry.insert(0, "https://docs.example.com")
        assert app.validate_url() == True
        
        # Invalid URL
        app.url_entry.delete(0, tk.END)
        app.url_entry.insert(0, "not-a-url")
        assert app.validate_url() == False
    
    @patch('DocScraperGUI.DocumentationScraper')
    def test_start_scraping(self, mock_scraper, app):
        """Test starting scraping from GUI."""
        app.url_entry.insert(0, "https://docs.example.com")
        app.max_pages_var.set(10)
        
        app.start_scraping()
        
        assert app.is_scraping == True
        assert app.start_button['state'] == 'disabled'
        mock_scraper.assert_called_once()
```

### Performance Test Example

```python
# tests/test_performance.py
import pytest
import time
import psutil
import asyncio
from DocPostProcessor import DocumentStructurer

class TestPerformance:
    
    @pytest.mark.performance
    def test_chunking_speed(self):
        """Test document chunking performance."""
        # Create large document
        large_doc = "# Test Document\n\n" + ("Lorem ipsum " * 1000 + "\n\n") * 100
        
        structurer = DocumentStructurer(chunk_size=1000)
        
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        chunks = structurer.create_chunks(large_doc)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        duration = end_time - start_time
        memory_used = end_memory - start_memory
        
        # Performance assertions
        assert duration < 5.0  # Should complete in under 5 seconds
        assert memory_used < 100  # Should use less than 100MB
        assert len(chunks) > 0
        
        print(f"Chunking performance: {duration:.2f}s, {memory_used:.2f}MB")
    
    @pytest.mark.performance
    @pytest.mark.slow
    async def test_concurrent_scraping(self):
        """Test concurrent scraping performance."""
        from DocScraper import DocumentationScraper
        
        scraper = DocumentationScraper()
        urls = [f"https://example.com/page{i}" for i in range(10)]
        
        start_time = time.time()
        
        # Simulate concurrent scraping
        tasks = [scraper._fetch_page(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        duration = time.time() - start_time
        
        # Should complete 10 pages in under 10 seconds (parallel)
        assert duration < 10.0
        print(f"Scraped {len(urls)} pages in {duration:.2f}s")
```

## Test Fixtures

### Sample Documents

```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_markdown():
    """Provide sample markdown content."""
    return """
# Sample Documentation

## Introduction
This is a test document for unit testing.

## Getting Started
1. Install the package
2. Configure settings
3. Run the application

## Code Example
```python
def hello_world():
    print("Hello, World!")
```

## Conclusion
Thanks for reading!
"""

@pytest.fixture
def sample_html():
    """Provide sample HTML content."""
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <nav>Navigation Menu</nav>
        <main>
            <h1>Test Page</h1>
            <p>This is test content.</p>
        </main>
        <footer>Footer content</footer>
    </body>
    </html>
    """

@pytest.fixture
def mock_api_response():
    """Mock OpenAI API response."""
    return {
        "choices": [{
            "message": {
                "content": "Category: guides\nComplexity: 0.3"
            }
        }]
    }
```

## Mocking External Services

### Mock Web Server

```python
# tests/utils/mock_server.py
from aiohttp import web
import asyncio

class MockDocumentationServer:
    """Mock server for testing web scraping."""
    
    def __init__(self, port=8888):
        self.port = port
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Set up mock routes."""
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/guide', self.guide)
        self.app.router.add_get('/api', self.api_docs)
    
    async def index(self, request):
        """Mock index page."""
        html = """
        <html>
        <body>
            <h1>Documentation</h1>
            <a href="/guide">Guide</a>
            <a href="/api">API</a>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')
    
    async def guide(self, request):
        """Mock guide page."""
        html = "<html><body><h1>Guide</h1><p>Content</p></body></html>"
        return web.Response(text=html, content_type='text/html')
    
    async def api_docs(self, request):
        """Mock API documentation."""
        html = "<html><body><h1>API</h1><p>Endpoints</p></body></html>"
        return web.Response(text=html, content_type='text/html')
    
    async def start(self):
        """Start the mock server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        return runner
```

### Mock OpenAI API

```python
# tests/utils/mock_openai.py
from unittest.mock import Mock

def mock_openai_client():
    """Create a mock OpenAI client."""
    client = Mock()
    
    # Mock completion response
    client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(message=Mock(content="Category: guides"))
        ]
    )
    
    # Mock embedding response
    client.embeddings.create.return_value = Mock(
        data=[
            Mock(embedding=[0.1] * 1536)
        ]
    )
    
    return client
```

## Coverage Reports

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Open HTML report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

### Coverage Configuration

Create `.coveragerc`:

```ini
[run]
source = .
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */site-packages/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstract

[html]
directory = htmlcov
```

## Continuous Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11, 3.12, 3.13]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio
        playwright install chromium
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

## Test Data Management

### Creating Test Fixtures

```python
# tests/fixtures/create_test_data.py
import json
from pathlib import Path

def create_test_documents():
    """Create test documentation files."""
    test_dir = Path("tests/fixtures/sample_docs")
    test_dir.mkdir(exist_ok=True)
    
    # Create various test documents
    docs = {
        "index.md": "# Documentation\n\nWelcome to the docs.",
        "getting-started.md": "# Getting Started\n\nQuick start guide.",
        "api-reference.md": "# API Reference\n\nAPI documentation.",
        "troubleshooting.md": "# Troubleshooting\n\nCommon issues."
    }
    
    for filename, content in docs.items():
        (test_dir / filename).write_text(content)
    
    # Create metadata file
    metadata = {
        "total_files": len(docs),
        "categories": ["guides", "api", "troubleshooting"]
    }
    
    (test_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    create_test_documents()
```

## Known Issues and Gaps

### Current Test Coverage Gaps

1. **GUI Testing**: Limited automated GUI testing
2. **Browser Testing**: Playwright browser automation tests needed
3. **Error Recovery**: More tests for error handling paths
4. **Performance**: Need more comprehensive performance benchmarks
5. **LLM Integration**: Mock testing for OpenAI API calls

### Testing TODOs

- [ ] Add property-based testing with Hypothesis
- [ ] Implement mutation testing
- [ ] Add load testing for concurrent operations
- [ ] Create visual regression tests for GUI
- [ ] Add security testing (fuzzing, injection)
- [ ] Implement contract testing for API
- [ ] Add accessibility testing for GUI
- [ ] Create integration tests with real vector databases

## Best Practices

1. **Write tests first**: Follow TDD when adding new features
2. **Keep tests fast**: Mock external dependencies
3. **Test edge cases**: Include boundary conditions
4. **Use fixtures**: Share common test data
5. **Clear test names**: Describe what is being tested
6. **One assertion per test**: Keep tests focused
7. **Clean up resources**: Use fixtures with teardown
8. **Mark slow tests**: Use pytest marks for categorization
9. **Test documentation**: Ensure examples in docs work
10. **Regular coverage checks**: Maintain coverage targets