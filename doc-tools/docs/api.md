# API Documentation

## Python API Reference

This document describes the public API for integrating DocScraper components into your Python applications.

## Core Classes

### DocumentationScraper

Main class for web scraping operations.

```python
from DocScraper import DocumentationScraper

scraper = DocumentationScraper(output_dir="scraped_docs")
```

#### Methods

##### `__init__(output_dir: str = "scraped_docs")`
Initialize the scraper with an output directory.

**Parameters:**
- `output_dir` (str): Directory to save scraped content. Default: "scraped_docs"

##### `async crawl_documentation(start_url: str, max_pages: int = 100) -> dict`
Crawl documentation starting from the given URL.

**Parameters:**
- `start_url` (str): The starting URL for crawling
- `max_pages` (int): Maximum number of pages to crawl. Default: 100

**Returns:**
- `dict`: Summary of the crawling operation
  ```python
  {
      "total_pages": 150,
      "successful": 145,
      "failed": 5,
      "failed_urls": ["url1", "url2", ...],
      "duration": 120.5,
      "output_dir": "scraped_docs"
  }
  ```

**Example:**
```python
import asyncio
from DocScraper import DocumentationScraper

async def main():
    scraper = DocumentationScraper("anthropic_docs")
    result = await scraper.crawl_documentation(
        "https://docs.anthropic.com",
        max_pages=200
    )
    print(f"Scraped {result['successful']} pages")

asyncio.run(main())
```

### DocumentPostProcessor

Main class for document post-processing.

```python
from DocPostProcessor import DocumentPostProcessor

processor = DocumentPostProcessor(
    input_dir="scraped_docs",
    output_dir="processed_docs",
    api_key="sk-..."  # Optional
)
```

#### Methods

##### `__init__(input_dir: str, output_dir: str, api_key: Optional[str] = None)`
Initialize the post-processor.

**Parameters:**
- `input_dir` (str): Directory containing scraped markdown files
- `output_dir` (str): Directory for processed output
- `api_key` (Optional[str]): OpenAI API key for LLM features

##### `async process_all_documents(process_subfolders: bool = True, flatten_output: bool = True) -> dict`
Process all documents in the input directory.

**Parameters:**
- `process_subfolders` (bool): Process subdirectories recursively. Default: True
- `flatten_output` (bool): Flatten output structure. Default: True

**Returns:**
- `dict`: Processing summary
  ```python
  {
      "total_documents": 150,
      "total_chunks": 1500,
      "categories": {
          "getting_started": 10,
          "guides": 45,
          "api_reference": 60,
          "concepts": 35
      },
      "processing_time": 45.2,
      "output_paths": {
          "cleaned": "processed_docs/cleaned",
          "chunks": "processed_docs/chunks",
          "vector_db": "processed_docs/vector_db_index.json"
      }
  }
  ```

**Example:**
```python
import asyncio
from DocPostProcessor import DocumentPostProcessor

async def main():
    processor = DocumentPostProcessor(
        "scraped_docs",
        "processed_docs",
        api_key="sk-..."
    )
    result = await processor.process_all_documents()
    print(f"Created {result['total_chunks']} chunks")

asyncio.run(main())
```

### DocumentCleaner

Utility class for cleaning markdown content.

```python
from DocPostProcessor import DocumentCleaner

cleaner = DocumentCleaner()
```

#### Methods

##### `clean_markdown(content: str) -> str`
Remove navigation elements and clean markdown content.

**Parameters:**
- `content` (str): Raw markdown content

**Returns:**
- `str`: Cleaned markdown content

##### `remove_navigation(content: str) -> str`
Remove navigation-specific elements.

**Parameters:**
- `content` (str): Markdown content

**Returns:**
- `str`: Content without navigation

##### `extract_metadata(content: str) -> dict`
Extract metadata from markdown content.

**Parameters:**
- `content` (str): Markdown content

**Returns:**
- `dict`: Extracted metadata
  ```python
  {
      "title": "Page Title",
      "description": "Page description",
      "tags": ["tag1", "tag2"],
      "last_modified": "2024-01-28"
  }
  ```

### DocumentStructurer

Class for creating document chunks.

```python
from DocPostProcessor import DocumentStructurer

structurer = DocumentStructurer(
    chunk_size=1000,
    chunk_overlap=200
)
```

#### Methods

##### `__init__(chunk_size: int = 1000, chunk_overlap: int = 200)`
Initialize the structurer.

**Parameters:**
- `chunk_size` (int): Target size for chunks in tokens
- `chunk_overlap` (int): Overlap between chunks in tokens

##### `create_chunks(content: str, metadata: dict = None) -> List[dict]`
Create chunks from document content.

**Parameters:**
- `content` (str): Document content
- `metadata` (dict): Optional metadata to attach to chunks

**Returns:**
- `List[dict]`: List of chunk dictionaries
  ```python
  [
      {
          "chunk_id": "doc1_chunk_0",
          "content": "Chunk content...",
          "metadata": {
              "source": "doc1.md",
              "chunk_index": 0,
              "total_chunks": 5,
              ...
          }
      },
      ...
  ]
  ```

### DocumentSorter

Class for categorizing and sorting documents.

```python
from DocPostProcessor import DocumentSorter

sorter = DocumentSorter(api_key="sk-...")  # Optional
```

#### Methods

##### `__init__(api_key: Optional[str] = None)`
Initialize the sorter.

**Parameters:**
- `api_key` (Optional[str]): OpenAI API key for LLM classification

##### `categorize_documents(documents: List[dict]) -> dict`
Categorize documents by type.

**Parameters:**
- `documents` (List[dict]): List of document dictionaries

**Returns:**
- `dict`: Categorized documents
  ```python
  {
      "getting_started": [...],
      "guides": [...],
      "api_reference": [...],
      "concepts": [...]
  }
  ```

##### `calculate_complexity(document: dict) -> float`
Calculate complexity score for a document.

**Parameters:**
- `document` (dict): Document dictionary

**Returns:**
- `float`: Complexity score (0.0 to 1.0)

##### `order_by_dependencies(documents: List[dict]) -> List[dict]`
Order documents by their dependencies.

**Parameters:**
- `documents` (List[dict]): List of documents

**Returns:**
- `List[dict]`: Ordered list of documents

## GUI API

### DocScraperGUI

GUI application for web scraping.

```python
from DocScraperGUI import DocScraperGUI

app = DocScraperGUI()
app.run()
```

### DocPostProcessorGUI

GUI application for post-processing.

```python
from DocPostProcessorGUI import DocPostProcessorGUI

app = DocPostProcessorGUI()
app.run()
```

## Command-Line Interface

### Scraping

```bash
# Basic usage
python DocScraper.py <url> [output_dir] [max_pages]

# Examples
python DocScraper.py https://docs.example.com
python DocScraper.py https://docs.example.com my_docs 500
```

### Post-Processing

```bash
# Basic usage
python DocPostProcessor.py <input_dir> <output_dir> [--use-llm]

# Examples
python DocPostProcessor.py scraped_docs processed_docs
python DocPostProcessor.py scraped_docs processed_docs --use-llm
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI API Key (for LLM features)
OPENAI_API_KEY=sk-...

# Optional: Custom settings
MAX_CONCURRENT_REQUESTS=5
RATE_LIMIT_DELAY=1.0
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Configuration Object

```python
from DocScraper import ScraperConfig

config = ScraperConfig(
    max_pages=200,
    concurrent_limit=5,
    rate_limit_delay=1.0,
    cache_mode="bypass",
    timeout=30000,
    user_agent="DocScraper/1.0"
)

scraper = DocumentationScraper(config=config)
```

## Error Handling

### Exception Types

```python
from DocScraper.exceptions import (
    ScrapingError,
    NetworkError,
    ParseError,
    StorageError
)

try:
    await scraper.crawl_documentation(url)
except NetworkError as e:
    print(f"Network issue: {e}")
except ScrapingError as e:
    print(f"Scraping failed: {e}")
```

### Error Recovery

```python
# Automatic retry with exponential backoff
scraper = DocumentationScraper(
    retry_attempts=3,
    retry_delay=2.0,
    exponential_backoff=True
)

# Manual error handling
result = await scraper.crawl_documentation(url)
if result['failed_urls']:
    # Retry failed URLs
    for url in result['failed_urls']:
        await scraper.crawl_single_page(url)
```

## Async Context Manager

```python
async with DocumentationScraper() as scraper:
    result = await scraper.crawl_documentation(url)
    # Resources automatically cleaned up
```

## Batch Processing

```python
# Process multiple documentation sites
urls = [
    "https://docs.site1.com",
    "https://docs.site2.com",
    "https://docs.site3.com"
]

async def batch_scrape(urls):
    tasks = []
    for url in urls:
        scraper = DocumentationScraper(
            output_dir=f"docs_{urlparse(url).netloc}"
        )
        tasks.append(scraper.crawl_documentation(url))
    
    results = await asyncio.gather(*tasks)
    return results
```

## Vector Database Integration

### Export Format

The post-processor generates a `vector_db_index.json` file:

```python
import json

with open("processed_docs/vector_db_index.json") as f:
    chunks = json.load(f)

for chunk in chunks:
    chunk_id = chunk["chunk_id"]
    content = chunk["content"]
    metadata = chunk["metadata"]
    
    # Generate embedding
    embedding = generate_embedding(content)
    
    # Store in vector DB
    vector_db.upsert(
        id=chunk_id,
        values=embedding,
        metadata=metadata
    )
```

### Integration Examples

#### Pinecone
```python
import pinecone
from DocPostProcessor import create_vector_index

index = pinecone.Index("documentation")
vector_data = create_vector_index("processed_docs")

for item in vector_data:
    index.upsert(
        vectors=[(item["id"], item["embedding"], item["metadata"])]
    )
```

#### ChromaDB
```python
import chromadb
from DocPostProcessor import load_chunks

client = chromadb.Client()
collection = client.create_collection("documentation")

chunks = load_chunks("processed_docs")
collection.add(
    documents=[c["content"] for c in chunks],
    metadatas=[c["metadata"] for c in chunks],
    ids=[c["chunk_id"] for c in chunks]
)
```

## Rate Limiting

### Built-in Rate Limiter

```python
from DocScraper import RateLimiter

rate_limiter = RateLimiter(
    max_requests_per_second=2,
    max_requests_per_minute=100
)

scraper = DocumentationScraper(rate_limiter=rate_limiter)
```

### Custom Rate Limiting

```python
class CustomRateLimiter:
    async def acquire(self):
        # Custom logic
        await asyncio.sleep(0.5)
    
    def release(self):
        # Cleanup if needed
        pass

scraper = DocumentationScraper(
    rate_limiter=CustomRateLimiter()
)
```

## Monitoring and Callbacks

### Progress Callbacks

```python
def on_page_scraped(url, success, error=None):
    if success:
        print(f"✓ Scraped: {url}")
    else:
        print(f"✗ Failed: {url} - {error}")

scraper = DocumentationScraper(
    callbacks={
        "on_page_scraped": on_page_scraped,
        "on_link_discovered": lambda url: print(f"Found: {url}"),
        "on_complete": lambda stats: print(f"Done: {stats}")
    }
)
```

### Custom Monitors

```python
from DocScraper import Monitor

class CustomMonitor(Monitor):
    def on_start(self, url):
        print(f"Starting: {url}")
    
    def on_progress(self, current, total):
        print(f"Progress: {current}/{total}")
    
    def on_error(self, error):
        print(f"Error: {error}")

scraper = DocumentationScraper(monitor=CustomMonitor())
```

## Performance Tips

1. **Concurrent Requests**: Adjust based on target server capacity
2. **Chunk Size**: Balance between context and token limits
3. **Cache Mode**: Use "write" for development, "bypass" for production
4. **Memory Management**: Process large sites in batches
5. **API Rate Limits**: Monitor OpenAI API usage for LLM features