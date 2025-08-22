# Empty Vector Database

This directory contains the empty vector database structure ready for your documentation.

## Structure

```
vector_db/
├── chunks/           # Document chunks storage
├── embeddings/       # Vector embeddings cache  
├── metadata/         # Document metadata
├── indices/          # Search indices
└── config/           # Database configuration
```

## Usage

The database will be populated when you:

1. Run the Claude Code documentation auto-scraper (during installation)
2. Use the doc-tools to scrape your own documentation
3. Manually import documentation via the MCP server

## Configuration

Default settings are optimized for:
- Semantic search across technical documentation
- Agent observation storage and retrieval
- Cross-project improvement tracking
- Real-time performance analysis

## Size

- Empty database: ~10MB (structure + indices)
- With Claude Code docs: ~50MB (testing data)
- Full documentation set: Varies by content (typically 100-500MB)

## Access

Access via:
- MCP Vector Server (`mcp-vector-server`)
- Claude Code integration (automatic)
- Direct API calls (for custom applications)