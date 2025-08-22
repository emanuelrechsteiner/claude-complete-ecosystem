# Documentation Scraper & Post-Processor

A comprehensive toolkit for scraping documentation websites and post-processing them for optimal use in vector databases and LLM applications.

## Features

### Scraping Features
- **Automatic URL Discovery**: Automatically discovers and crawls all documentation pages on a domain
- **Markdown Conversion**: Converts HTML content to clean markdown format
- **Domain Limiting**: Stays within the specified domain to avoid crawling external sites
- **Progress Tracking**: Real-time progress updates and summary statistics
- **Error Handling**: Gracefully handles failed pages and continues crawling
- **Rate Limiting**: Built-in delays to avoid overwhelming servers

### Post-Processing Features (NEW!)
- **Document Cleaning**: Removes headers, footers, navigation elements, and duplicate content
- **Smart Structuring**: Creates hierarchical chunks optimized for embeddings
- **LLM-Powered Sorting**: Uses AI to categorize and order documents for optimal learning
- **Vector DB Optimization**: Prepares content for efficient vector database ingestion
- **Dependency Analysis**: Identifies relationships between documents
- **Complexity Scoring**: Ranks documents by complexity for progressive learning
- **Multi-Folder Processing**: Process entire directory trees with multiple subfolders
- **Output Consolidation**: Flatten all processed files into a single output directory

### GUI Features
- **User-Friendly Interface**: Built with Tkinter
- **Real-Time Logging**: See what's happening as it processes
- **Configuration Options**: Easy adjustment of all parameters
- **Progress Visualization**: Progress bars and statistics
- **Thread-Safe Operation**: Stable multi-threaded processing

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. (Optional) Set up environment variables for LLM features:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## Usage

### Web Scraping

#### Command Line
Basic usage:
```bash
python SimpleDocScraper.py <documentation_url>
```

With options:
```bash
python SimpleDocScraper.py <documentation_url> <output_dir> <max_pages>
```

Examples:
```bash
# Scrape Anthropic documentation
python SimpleDocScraper.py https://docs.anthropic.com

# Scrape with custom settings
python SimpleDocScraper.py https://docs.anthropic.com anthropic_docs 500
```

#### GUI Version
For a graphical interface:
```bash
python DocScraperGUI.py
```

### Document Post-Processing

#### Command Line
Basic usage (rule-based classification):
```bash
python DocPostProcessor.py <input_dir> <output_dir>
```

With LLM classification:
```bash
python DocPostProcessor.py <input_dir> <output_dir> --use-llm
```

Examples:
```bash
# Process scraped Anthropic docs
python DocPostProcessor.py Documentation/Anthropic processed_docs

# Process with AI classification
python DocPostProcessor.py Documentation/Anthropic processed_docs --use-llm
```

#### GUI Version
For a graphical interface:
```bash
python DocPostProcessorGUI.py
```

#### Example Scripts
Run the comprehensive examples:
```bash
# Basic processing example
python process_docs_example.py

# Multi-folder processing example
python process_multi_folder_example.py
```

## Post-Processing Pipeline

### 1. Cleaning Phase
- Removes navigation elements, headers, and footers
- Strips duplicate content and boilerplate text
- Preserves important structure (code blocks, lists, tables)
- Extracts and preserves metadata

### 2. Structuring Phase
- Parses document hierarchy (headers, sections)
- Creates semantic chunks with configurable size
- Implements smart overlap for context preservation
- Tags chunks with metadata for better retrieval

### 3. Sorting Phase
- Categorizes documents (getting started, guides, API reference, etc.)
- Analyzes dependencies between documents
- Calculates complexity scores
- Orders documents for optimal learning progression

## Multi-Folder Processing

The post-processor can handle complex directory structures with multiple subfolders:

### Input Structure Example
```
Documentation/
├── Anthropic/
│   ├── guides/
│   │   ├── getting-started.md
│   │   └── advanced-usage.md
│   ├── api/
│   │   └── endpoints.md
│   └── concepts.md
├── React/
│   ├── hooks/
│   │   ├── useState.md
│   │   └── useEffect.md
│   └── components.md
└── Shadcn/
    └── ui-components.md
```

### Processing Options
1. **Recursive Processing**: Process all files in all subdirectories
2. **Flatten Output**: Consolidate all processed files into a single output directory
3. **Preserve Structure**: Maintain folder hierarchy in output (optional)

### Output with Flattening
```
processed_docs/
├── cleaned/
│   ├── 0000_Anthropic_guides_getting-started.md
│   ├── 0001_Anthropic_guides_advanced-usage.md
│   ├── 0002_Anthropic_api_endpoints.md
│   ├── 0003_Anthropic_concepts.md
│   ├── 0004_React_hooks_useState.md
│   └── ...
├── chunks/
│   └── [corresponding chunk directories]
├── processing_summary.json
└── vector_db_index.json
```

The flattened output preserves source folder information in filenames while consolidating everything for easier vector database ingestion.

## Output Structure

### Scraping Output
```
scraped_docs/
├── index.md
├── getting-started.md
├── api_reference.md
└── _scrape_summary.json
```

### Post-Processing Output
```
processed_docs/
├── cleaned/           # Cleaned full documents
│   ├── 0000_index.md
│   ├── 0001_getting_started.md
│   └── ...
├── chunks/           # Document chunks for embedding
│   ├── 0000_index/
│   │   ├── chunk_000.json
│   │   └── chunk_001.json
│   └── ...
├── metadata/         # Document metadata
├── processing_summary.json
└── vector_db_index.json  # Ready for vector database
```

## Vector Database Integration

The post-processor creates a `vector_db_index.json` file optimized for vector database ingestion:

```json
[
  {
    "chunk_id": "a1b2c3d4",
    "content": "Chunk content here...",
    "metadata": {
      "source_url": "https://docs.example.com/page",
      "title": "Page Title",
      "category": "guides",
      "complexity": 0.45,
      "section_title": "Section Name"
    }
  }
]
```

### Next Steps for Vector DB:
1. Load the `vector_db_index.json` file
2. Generate embeddings using your preferred model
3. Store in your vector database (Pinecone, Weaviate, ChromaDB, etc.)
4. Implement semantic search over the documentation

## Configuration Options

### Scraper Configuration
- `max_pages`: Maximum number of pages to crawl
- `output_dir`: Directory for saving scraped content
- Rate limiting and concurrent crawl settings

### Post-Processor Configuration
- `chunk_size`: Target size for document chunks (default: 1000 tokens)
- `chunk_overlap`: Overlap between chunks (default: 200 tokens)
- `use_llm`: Enable AI-powered classification (requires API key)
- `process_subfolders`: Process all subdirectories recursively (default: True)
- `flatten_output`: Consolidate all output files in single directory (default: True)

## Tips & Best Practices

### For Scraping
1. **Start Small**: Test with a low `max_pages` value first
2. **Check Robots.txt**: Ensure you're allowed to crawl the target site
3. **Monitor Progress**: Watch the console output for any issues
4. **Review Output**: Check the `_scrape_summary.json` for failed URLs

### For Post-Processing
1. **Clean First**: Always run post-processing on scraped docs before vector DB ingestion
2. **Tune Chunk Size**: Adjust based on your embedding model's context window
3. **Use LLM Classification**: Provides better categorization than rule-based
4. **Review Categories**: Check the processing summary to ensure proper classification

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed in the virtual environment
2. **Network Errors**: Check your internet connection and the target site's availability
3. **Rate Limiting**: If getting 429 errors, increase delays in the scraper
4. **Memory Issues**: For large documentation sets, process in batches
5. **API Key Errors**: Ensure your OpenAI API key is set correctly in `.env`

### Performance Optimization

- For large documentation sets, consider processing in batches
- Adjust chunk size based on your use case and embedding model
- Use the GUI for better progress monitoring
- Enable parallel processing in the advanced scraper

## Architecture

### Components
1. **DocScraper.py**: Advanced scraper with parallel processing
2. **SimpleDocScraper.py**: Simplified sequential scraper
3. **DocScraperGUI.py**: Tkinter GUI for scraping
4. **DocPostProcessor.py**: Core post-processing engine
5. **DocPostProcessorGUI.py**: Tkinter GUI for post-processing

### Key Classes
- `DocumentationScraper`: Handles web crawling and content extraction
- `DocumentCleaner`: Removes unwanted elements from markdown
- `DocumentStructurer`: Creates optimized chunks for embeddings
- `DocumentSorter`: Categorizes and orders documents using AI/rules

## License

This tool is for educational and personal use. Always respect website terms of service and robots.txt files.
