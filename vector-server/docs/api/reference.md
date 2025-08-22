# API Reference

## Overview

The MCP Vector Server implements the Model Context Protocol (MCP) specification, providing semantic search capabilities through standardized endpoints. This API enables intelligent documentation retrieval across multiple technology stacks.

## Base Configuration

### Server Connection
```json
{
  "mcpServers": {
    "vector-search": {
      "command": "uv",
      "args": ["run", "mcp-vector-server"],
      "env": {
        "VECTOR_DB_PATH": "/path/to/vector/database"
      }
    }
  }
}
```

## Core Endpoints

### 1. Search Documentation

**Tool Name**: `search_documentation`

**Description**: Performs semantic search across indexed documentation chunks using natural language queries.

**Parameters**:
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `query` | string | Yes | Natural language search query | - |
| `limit` | integer | No | Maximum number of results | 10 |
| `category` | string | No | Filter by documentation category | null |
| `technology` | string | No | Filter by technology stack | null |
| `doc_type` | string | No | Filter by document type (text/code) | null |
| `min_similarity` | float | No | Minimum similarity threshold (0.0-1.0) | 0.3 |

**Example Request**:
```json
{
  "tool": "search_documentation",
  "arguments": {
    "query": "How to implement authentication in Convex?",
    "limit": 5,
    "category": "guides",
    "technology": "Convex"
  }
}
```

**Response Structure**:
```json
{
  "results": [
    {
      "chunk": {
        "chunk_id": "convex_auth_001",
        "content": "To implement authentication in Convex...",
        "metadata": {
          "type": "text",
          "source_url": "https://docs.convex.dev/auth",
          "doc_title": "Authentication Guide",
          "category": "guides",
          "complexity": 0.6,
          "section_title": "Setting up Auth"
        },
        "position": 1,
        "tokens": 256
      },
      "similarity": 0.92,
      "rank": 1
    }
  ],
  "query_metadata": {
    "processed_query": "implement authentication convex",
    "total_results": 5,
    "search_time_ms": 120
  }
}
```

### 2. Get Categories

**Tool Name**: `get_categories`

**Description**: Returns all available documentation categories with descriptions.

**Parameters**: None

**Response**:
```json
{
  "categories": {
    "getting_started": "Quick start guides and installation instructions",
    "concepts": "Core concepts and architectural explanations",
    "guides": "Step-by-step tutorials and how-to guides",
    "api_reference": "API documentation and reference materials",
    "examples": "Code examples and sample implementations",
    "advanced": "Advanced topics and detailed configurations",
    "troubleshooting": "Common issues and solutions",
    "mcp": "Model Context Protocol related documentation",
    "setup": "Installation and setup instructions",
    "authentication": "Authentication and security documentation"
  }
}
```

### 3. Get Technologies

**Tool Name**: `get_technologies`

**Description**: Returns all supported technology stacks with metadata.

**Parameters**: None

**Response**:
```json
{
  "technologies": [
    {
      "name": "Convex",
      "keywords": ["convex", "database", "backend", "realtime"],
      "categories": ["getting_started", "guides", "api_reference"],
      "doc_count": 5420
    },
    {
      "name": "Shadcn/ui",
      "keywords": ["shadcn", "ui", "components", "design system"],
      "categories": ["getting_started", "guides", "examples"],
      "doc_count": 3200
    }
  ]
}
```

### 4. Get Chunk by ID

**Tool Name**: `get_chunk`

**Description**: Retrieves a specific documentation chunk by its unique identifier.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chunk_id` | string | Yes | Unique chunk identifier |

**Response**:
```json
{
  "chunk": {
    "chunk_id": "convex_auth_001",
    "content": "Full chunk content...",
    "metadata": {
      "type": "text",
      "source_url": "https://docs.convex.dev/auth",
      "doc_title": "Authentication Guide",
      "category": "guides"
    }
  }
}
```

## Advanced Search Features

### Similarity Search

The server uses cosine similarity for semantic matching:
- **1.0**: Exact semantic match
- **0.8-1.0**: Highly relevant
- **0.6-0.8**: Relevant
- **0.3-0.6**: Somewhat relevant
- **< 0.3**: Low relevance (filtered by default)

### Query Processing

Queries are processed through:
1. **Tokenization**: Breaking down into semantic components
2. **Embedding**: Converting to vector representation
3. **Similarity Matching**: Finding closest vectors in database
4. **Ranking**: Ordering by relevance score
5. **Filtering**: Applying category/technology constraints

### Category Filtering

Available categories:
- `getting_started` - Installation and setup
- `guides` - How-to tutorials
- `api_reference` - API documentation
- `concepts` - Core concepts
- `examples` - Code samples
- `advanced` - Advanced topics
- `troubleshooting` - Problem solving
- `mcp` - MCP-specific docs
- `authentication` - Auth/security

### Technology Filtering

Supported technologies:
- `Convex` - Backend database
- `Shadcn/ui` - Component library
- `RadixUI` - UI primitives
- `TailwindCSS` - Styling
- `React` - Frontend framework
- `Claude Code` - AI development
- `Kiro` - Development tools
- `Clerk` - Authentication
- `Polar` - Subscriptions

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query parameter is required",
    "details": {
      "field": "query",
      "provided": null
    }
  }
}
```

### Common Error Codes
| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_QUERY` | Query parameter missing or invalid | Provide valid query string |
| `INVALID_LIMIT` | Limit outside valid range (1-100) | Use limit between 1-100 |
| `INVALID_CATEGORY` | Unknown category specified | Use valid category from list |
| `INVALID_TECHNOLOGY` | Unknown technology specified | Use valid technology from list |
| `CHUNK_NOT_FOUND` | Requested chunk ID doesn't exist | Verify chunk ID |
| `DATABASE_ERROR` | Vector database unavailable | Check database path/connection |
| `EMBEDDING_ERROR` | Failed to generate embeddings | Check model availability |

## Rate Limiting

The server implements rate limiting to ensure fair usage:
- **Default**: 100 requests per minute
- **Burst**: Up to 10 concurrent requests
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Performance Considerations

### Optimization Tips
1. **Use specific queries**: More specific queries yield better results
2. **Apply filters**: Category/technology filters reduce search space
3. **Limit results**: Request only needed results (default: 10)
4. **Cache frequently used**: Consider caching common queries client-side

### Response Times
- **< 100ms**: Cached queries
- **100-300ms**: Standard queries
- **300-500ms**: Complex queries with filters
- **> 500ms**: Large result sets or cold starts

## Integration Examples

### Claude Code Configuration
```json
{
  "mcpServers": {
    "vector-search": {
      "command": "uv",
      "args": ["run", "mcp-vector-server"]
    }
  }
}
```

### Cursor IDE Setup
```json
{
  "mcp": {
    "servers": {
      "vector-search": {
        "command": "python",
        "args": ["-m", "mcp_vector_server"]
      }
    }
  }
}
```

### Programmatic Usage (Python)
```python
import mcp

client = mcp.Client("vector-search")
results = await client.call_tool(
    "search_documentation",
    {
        "query": "React hooks best practices",
        "limit": 5,
        "technology": "React"
    }
)
```

## Debugging

### Enable Debug Logging
```bash
export MCP_DEBUG=true
export LOG_LEVEL=debug
uv run mcp-vector-server
```

### Common Issues
1. **No results returned**: Check similarity threshold, try broader query
2. **Slow responses**: Verify vector database is loaded in memory
3. **Connection errors**: Ensure server is running and accessible
4. **Invalid results**: Verify query encoding and filters

## Versioning

The API follows semantic versioning:
- **Current Version**: 1.0.0
- **Protocol Version**: MCP 1.0
- **Backward Compatibility**: Maintained for major versions

## Support

For API issues or questions:
- GitHub Issues: [Report bugs](https://github.com/yourusername/mcp-vector-server)
- Documentation: [Full docs](../index.md)
- Examples: [Code samples](https://github.com/yourusername/mcp-vector-server/examples)