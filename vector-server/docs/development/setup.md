# Development Setup Guide

## Quick Start

Get up and running with the MCP Vector Server development environment in under 5 minutes.

```bash
# Clone and setup
git clone <repository-url>
cd mcp-vector-server
uv venv
source .venv/bin/activate
uv sync

# Start development server
uv run mcp-vector-server
```

## Prerequisites

### Required Software

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| Python | 3.10+ | Runtime environment | `brew install python` |
| UV | Latest | Package management | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Git | 2.30+ | Version control | `brew install git` |

### System Requirements

- **OS**: macOS, Linux, or Windows with WSL2
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: 2GB free space for dependencies and vector database
- **Network**: Internet access for downloading models and dependencies

## Environment Setup

### 1. Project Clone & Directory Setup

```bash
# Clone the repository
git clone <repository-url>
cd mcp-vector-server

# Verify project structure
tree -L 2
```

Expected structure:
```
mcp-vector-server/
├── src/
│   └── mcp_vector_server/
├── docs/
├── pyproject.toml
├── README.md
└── .gitignore
```

### 2. Python Environment

```bash
# Create virtual environment with UV
uv venv

# Activate environment (macOS/Linux)
source .venv/bin/activate

# Activate environment (Windows)
.venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.10+
```

### 3. Dependency Installation

```bash
# Install production dependencies
uv sync

# Install development dependencies
uv sync --dev

# Verify installation
uv run python -c "import mcp_vector_server; print('Setup complete!')"
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# .env file (copy from .env.example)
VECTOR_DB_PATH=/path/to/vector/database
MCP_SERVER_NAME=mcp-vector-server
LOG_LEVEL=INFO
SIMILARITY_THRESHOLD=0.3
MAX_RESULTS=100

# Optional: Development settings
MCP_DEBUG=true
RELOAD_ON_CHANGE=true
```

### Vector Database Setup

The server requires a pre-built vector database with documentation embeddings:

```bash
# Download sample database (replace with actual URL)
curl -L https://example.com/vector-db.tar.gz -o vector-db.tar.gz
tar -xzf vector-db.tar.gz

# Set path in .env
echo "VECTOR_DB_PATH=$(pwd)/vector-db" >> .env
```

**Note**: Contact the team for access to the full documentation database (~45K chunks).

## Development Workflow

### Running the Server

```bash
# Standard development mode
uv run mcp-vector-server

# With debug logging
MCP_DEBUG=true uv run mcp-vector-server

# With auto-reload (if supported)
uv run --reload mcp-vector-server
```

### Testing the Installation

```bash
# Test basic functionality
echo '{"method": "tools/list"}' | uv run mcp-vector-server

# Expected output should list available tools
```

### IDE Integration Testing

Test your setup with IDE integration:

#### Claude Code
```json
{
  "mcpServers": {
    "vector-search": {
      "command": "uv",
      "args": ["run", "mcp-vector-server"],
      "cwd": "/path/to/mcp-vector-server"
    }
  }
}
```

#### VS Code with MCP Extension
```json
{
  "mcp.servers": [
    {
      "name": "vector-search",
      "command": "uv",
      "args": ["run", "mcp-vector-server"],
      "cwd": "/path/to/mcp-vector-server"
    }
  ]
}
```

## Development Tools

### Code Quality Tools

```bash
# Format code
uv run black src/
uv run isort src/

# Type checking
uv run mypy src/

# Linting (if configured)
uv run flake8 src/

# All quality checks
uv run python -m scripts.quality_check
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/mcp_vector_server

# Run specific test file
uv run pytest tests/test_models.py

# Run with debug output
uv run pytest -v -s
```

### Debugging

#### Debug Mode
```bash
# Enable comprehensive debugging
export MCP_DEBUG=true
export LOG_LEVEL=debug
uv run mcp-vector-server
```

#### Python Debugger
```python
# Add to code for breakpoints
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

#### Logging Configuration
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Common Development Tasks

### Adding New Dependencies

```bash
# Add production dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update all dependencies
uv sync --upgrade
```

### Database Operations

```bash
# Check database status
uv run python -c "
from src.mcp_vector_server.models import *
print('Database accessible')
"

# Rebuild embeddings (if needed)
uv run python scripts/rebuild_database.py
```

### Code Generation

```bash
# Generate API documentation
uv run python scripts/generate_docs.py

# Update type stubs
uv run stubgen -p mcp_vector_server -o stubs/
```

## Performance Optimization

### Memory Management

```bash
# Monitor memory usage during development
uv run python -m memory_profiler scripts/profile_search.py

# Run with memory constraints
export MALLOC_ARENA_MAX=2
uv run mcp-vector-server
```

### Profiling

```bash
# Profile search performance
uv run python -m cProfile -o profile.stats scripts/benchmark.py

# Analyze profile
uv run python -c "
import pstats
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative').print_stats(10)
"
```

## IDE-Specific Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort

`.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.formatting.provider": "black",
  "python.sortImports.args": ["--profile", "black"],
  "python.linting.mypyEnabled": true
}
```

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Add Existing Environment → `.venv/bin/python`
3. Enable Black and isort in Code Style settings

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Issue: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source .venv/bin/activate
uv sync
```

#### Permission Errors
```bash
# Issue: Permission denied on vector database
# Solution: Check file permissions
chmod -R 755 /path/to/vector-db
```

#### Memory Errors
```bash
# Issue: Out of memory during embedding
# Solution: Reduce batch size or increase swap
export EMBEDDING_BATCH_SIZE=100
```

#### Port Conflicts
```bash
# Issue: Port already in use
# Solution: Find and kill process or use different port
lsof -ti:8000 | xargs kill -9
export MCP_PORT=8001
```

### Debug Commands

```bash
# Check Python environment
which python
pip list

# Verify package installation
python -c "import mcp_vector_server; print(mcp_vector_server.__version__)"

# Test database connection
python -c "
import os
print(f'Vector DB path: {os.getenv(\"VECTOR_DB_PATH\")}')
print(f'Path exists: {os.path.exists(os.getenv(\"VECTOR_DB_PATH\", \"\"))}')
"

# Test embeddings
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode('test query')
print(f'Embedding shape: {embedding.shape}')
"
```

## Next Steps

After successful setup:

1. **Read the [Contributing Guide](./contributing.md)** for development workflow
2. **Review the [API Reference](../api/reference.md)** for endpoint details
3. **Check [Testing Guide](./testing.md)** for test procedures
4. **Join the development discussion** on GitHub Issues

## Getting Help

- **Documentation Issues**: Check [Troubleshooting Guide](./troubleshooting.md)
- **Setup Problems**: Create a GitHub issue with system details
- **Feature Requests**: Discuss in GitHub Discussions
- **Security Issues**: Follow [Security Guidelines](../deployment/security.md)

---

*Setup complete! Ready to start developing.* 🚀