"""MCP Vector Server main entry point."""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

import numpy as np
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool
from pydantic import BaseModel, Field

from .models import (
    SearchQuery,
    SearchResult,
    DocumentChunk,
    ChunkMetadata,
    TECH_MAPPINGS,
    CATEGORY_DESCRIPTIONS
)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VectorDatabase:
    """Simple vector database for demo purposes."""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("VECTOR_DB_PATH", "")
        self.chunks: List[DocumentChunk] = []
        self.embeddings: Optional[np.ndarray] = None
        self.loaded = False
        
    def load(self):
        """Load vector database."""
        if not self.db_path:
            logger.warning("No vector database path specified. Using demo data.")
            self._load_demo_data()
        else:
            try:
                self._load_from_path()
            except Exception as e:
                logger.warning(f"Failed to load database from {self.db_path}: {e}")
                logger.info("Falling back to demo data.")
                self._load_demo_data()
        
        self.loaded = True
    
    def _load_demo_data(self):
        """Load demo documentation chunks."""
        # Create sample chunks for demonstration
        demo_chunks = [
            DocumentChunk(
                chunk_id="react_001",
                content="React hooks like useState and useEffect allow you to use state and side effects in functional components. The useState hook returns a stateful value and a function to update it.",
                metadata=ChunkMetadata(
                    type="text",
                    category="guides",
                    doc_title="React Hooks Guide",
                    source_url="https://react.dev/hooks"
                ),
                tokens=30
            ),
            DocumentChunk(
                chunk_id="convex_001",
                content="Convex is a backend application platform with a built-in database that keeps your data in sync across all clients in real-time. It provides ACID transactions and automatic caching.",
                metadata=ChunkMetadata(
                    type="text",
                    category="getting_started",
                    doc_title="Convex Overview",
                    source_url="https://docs.convex.dev"
                ),
                tokens=28
            ),
            DocumentChunk(
                chunk_id="shadcn_001",
                content="Shadcn/ui provides copy-and-paste React components built with Radix UI and Tailwind CSS. Components are accessible, customizable, and open source.",
                metadata=ChunkMetadata(
                    type="text",
                    category="getting_started",
                    doc_title="Shadcn/ui Introduction",
                    source_url="https://ui.shadcn.com"
                ),
                tokens=25
            ),
            DocumentChunk(
                chunk_id="tailwind_001",
                content="TailwindCSS is a utility-first CSS framework. Use utility classes like flex, pt-4, text-center and rotate-90 to build any design directly in your markup.",
                metadata=ChunkMetadata(
                    type="text",
                    category="guides",
                    doc_title="TailwindCSS Basics",
                    source_url="https://tailwindcss.com"
                ),
                tokens=28
            ),
            DocumentChunk(
                chunk_id="clerk_001",
                content="Clerk provides authentication and user management. It includes pre-built UI components, APIs for user operations, and integrations with popular frameworks.",
                metadata=ChunkMetadata(
                    type="text",
                    category="authentication",
                    doc_title="Clerk Authentication",
                    source_url="https://clerk.dev"
                ),
                tokens=24
            )
        ]
        
        self.chunks = demo_chunks
        # Create simple embeddings for demo (normally would use sentence-transformers)
        self.embeddings = np.random.rand(len(demo_chunks), 768)
        logger.info(f"Loaded {len(self.chunks)} demo documentation chunks")
    
    def _load_from_path(self):
        """Load database from specified path."""
        db_path = Path(self.db_path)
        
        # Load vector database index
        index_file = db_path / "vector_db_index.json"
        if not index_file.exists():
            raise ValueError(f"Vector database index not found at {index_file}")
        
        with open(index_file, 'r') as f:
            db_index = json.load(f)
            logger.info(f"Loading vector database with {len(db_index)} entries")
            
            # Convert index to DocumentChunk objects
            self.chunks = []
            for idx, entry in enumerate(db_index):
                try:
                    chunk = DocumentChunk(
                        chunk_id=entry.get('chunk_id', f"chunk_{idx}"),
                        content=entry.get('content', ''),
                        metadata=ChunkMetadata(
                            type=entry.get('metadata', {}).get('type', 'text'),
                            category=entry.get('metadata', {}).get('category', 'guides'),
                            doc_title=entry.get('metadata', {}).get('doc_title', 'Unknown'),
                            source_url=entry.get('metadata', {}).get('source_url'),
                            source_file=entry.get('metadata', {}).get('source_file')
                        ),
                        tokens=entry.get('tokens', 0)
                    )
                    self.chunks.append(chunk)
                except Exception as e:
                    logger.warning(f"Failed to parse chunk {idx}: {e}")
                    continue
            
            # Create simple embeddings for demo (would normally load real embeddings)
            if self.chunks:
                self.embeddings = np.random.rand(len(self.chunks), 768)
                logger.info(f"Loaded {len(self.chunks)} chunks from real vector database")
            else:
                raise ValueError("No valid chunks found in database")
    
    def search(self, query: str, limit: int = 10, **filters) -> List[SearchResult]:
        """Perform semantic search."""
        if not self.loaded:
            self.load()
        
        # For demo, return random similarity scores
        # In production, would compute actual cosine similarity
        results = []
        
        for i, chunk in enumerate(self.chunks[:limit]):
            # Apply filters
            if filters.get("category") and chunk.metadata.category != filters["category"]:
                continue
            if filters.get("technology"):
                # Simple keyword matching for demo
                tech_lower = filters["technology"].lower()
                if tech_lower not in chunk.content.lower() and tech_lower not in (chunk.metadata.doc_title or "").lower():
                    continue
            
            # Create result with random similarity for demo
            similarity = np.random.uniform(0.7, 0.95)
            results.append(SearchResult(
                chunk=chunk,
                similarity=float(similarity),
                rank=len(results) + 1
            ))
        
        # Sort by similarity
        results.sort(key=lambda x: x.similarity, reverse=True)
        
        # Update ranks
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results[:limit]


# Initialize global database
vector_db = VectorDatabase()


async def main():
    """Run the MCP server."""
    logger.info("Starting MCP Vector Server...")
    
    # Create server instance
    server = Server("mcp-vector-server")
    
    # Load database on startup
    try:
        vector_db.load()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="search_documentation",
                description="Search technical documentation using natural language queries",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language search query"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (1-100)",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        },
                        "category": {
                            "type": "string",
                            "description": "Filter by documentation category",
                            "enum": list(CATEGORY_DESCRIPTIONS.keys())
                        },
                        "technology": {
                            "type": "string",
                            "description": "Filter by technology",
                            "enum": [tech.name for tech in TECH_MAPPINGS]
                        },
                        "min_similarity": {
                            "type": "number",
                            "description": "Minimum similarity threshold (0.0-1.0)",
                            "default": 0.3,
                            "minimum": 0.0,
                            "maximum": 1.0
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="get_categories",
                description="Get all available documentation categories",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_technologies",
                description="Get all supported technologies",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> Any:
        """Handle tool calls."""
        logger.debug(f"Tool called: {name} with arguments: {arguments}")
        
        if name == "search_documentation":
            try:
                # Validate query
                query = SearchQuery(**arguments)
                
                # Perform search
                results = vector_db.search(
                    query=query.query,
                    limit=query.limit,
                    category=query.category,
                    technology=query.technology
                )
                
                # Filter by similarity threshold
                filtered_results = [
                    r for r in results 
                    if r.similarity >= query.min_similarity
                ]
                
                # Format response
                return {
                    "results": [
                        {
                            "chunk": {
                                "chunk_id": r.chunk.chunk_id,
                                "content": r.chunk.content,
                                "metadata": r.chunk.metadata.dict(),
                                "tokens": r.chunk.tokens
                            },
                            "similarity": r.similarity,
                            "rank": r.rank
                        }
                        for r in filtered_results
                    ],
                    "query_metadata": {
                        "query": query.query,
                        "total_results": len(filtered_results),
                        "filters_applied": {
                            "category": query.category,
                            "technology": query.technology,
                            "min_similarity": query.min_similarity
                        }
                    }
                }
            except Exception as e:
                logger.error(f"Search error: {e}")
                return {"error": str(e)}
        
        elif name == "get_categories":
            return {"categories": CATEGORY_DESCRIPTIONS}
        
        elif name == "get_technologies":
            return {
                "technologies": [
                    {
                        "name": tech.name,
                        "keywords": tech.keywords,
                        "categories": tech.categories
                    }
                    for tech in TECH_MAPPINGS
                ]
            }
        
        else:
            return {"error": f"Unknown tool: {name}"}
    
    # Run the server with stdio
    logger.info("MCP Vector Server ready for connections")
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream)
    except Exception as e:
        logger.error(f"Server connection error: {e}")
        # Don't raise the error, let it complete gracefully


def run():
    """Entry point for the server."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()