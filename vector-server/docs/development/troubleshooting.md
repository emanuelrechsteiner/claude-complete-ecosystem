# Troubleshooting Guide

## Quick Diagnostic Commands

```bash
# Check system status
uv run python -c "import mcp_vector_server; print('✅ Package imported successfully')"
uv run python -c "import numpy, sentence_transformers; print('✅ Dependencies available')"

# Verify environment
echo "Python: $(python --version)"
echo "UV: $(uv --version)"
echo "Vector DB Path: ${VECTOR_DB_PATH:-'Not set'}"

# Test basic functionality
echo '{"method": "tools/list"}' | uv run mcp-vector-server
```

## Common Issues & Solutions

### Installation & Setup Issues

#### Issue: `ModuleNotFoundError: No module named 'mcp_vector_server'`

**Symptoms**:
```bash
$ uv run mcp-vector-server
ModuleNotFoundError: No module named 'mcp_vector_server'
```

**Causes & Solutions**:

1. **Virtual environment not activated**:
   ```bash
   # Solution
   source .venv/bin/activate
   uv sync
   ```

2. **Package not installed**:
   ```bash
   # Solution
   uv sync --dev
   uv run pip install -e .
   ```

3. **Wrong directory**:
   ```bash
   # Solution
   cd /path/to/mcp-vector-server
   ls -la  # Verify pyproject.toml exists
   ```

#### Issue: `Permission denied` errors

**Symptoms**:
```bash
PermissionError: [Errno 13] Permission denied: '/path/to/vector-db'
```

**Solutions**:
```bash
# Fix file permissions
chmod -R 755 /path/to/vector-database
chown -R $USER:$USER /path/to/vector-database

# Or use different path
export VECTOR_DB_PATH="$HOME/vector-database"
```

#### Issue: UV installation problems

**Symptoms**:
```bash
uv: command not found
```

**Solutions**:
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Or via pip
pip install uv

# Verify installation
uv --version
```

### Vector Database Issues

#### Issue: `Database file not found` or `VECTOR_DB_PATH not set`

**Symptoms**:
```bash
FileNotFoundError: Vector database not found at path: None
```

**Solutions**:

1. **Set environment variable**:
   ```bash
   export VECTOR_DB_PATH="/path/to/vector/database"
   # Or create .env file
   echo "VECTOR_DB_PATH=/path/to/vector/database" > .env
   ```

2. **Download/create database**:
   ```bash
   # Contact team for database download link
   curl -L https://example.com/vector-db.tar.gz -o vector-db.tar.gz
   tar -xzf vector-db.tar.gz
   export VECTOR_DB_PATH="$(pwd)/vector-db"
   ```

3. **Verify database structure**:
   ```bash
   ls -la $VECTOR_DB_PATH
   # Should contain: embeddings.npy, chunks.json, metadata.json
   ```

#### Issue: `Invalid database format` or corruption

**Symptoms**:
```bash
ValueError: Invalid database format, expected version 1.0
```

**Solutions**:
```bash
# Check database integrity
uv run python -c "
import numpy as np
try:
    embeddings = np.load('$VECTOR_DB_PATH/embeddings.npy')
    print(f'Embeddings shape: {embeddings.shape}')
except Exception as e:
    print(f'Database error: {e}')
"

# Rebuild database (if rebuild script available)
uv run python scripts/rebuild_database.py

# Or contact team for fresh database copy
```

### Search & Embedding Issues

#### Issue: `No results found` for valid queries

**Symptoms**:
```bash
# Query returns empty results despite valid input
results = search_documentation("React hooks")
# len(results) == 0
```

**Debugging Steps**:

1. **Check similarity threshold**:
   ```python
   # Lower the threshold
   results = search_documentation(
       "React hooks", 
       min_similarity=0.1  # Very permissive
   )
   ```

2. **Verify embeddings**:
   ```python
   from src.mcp_vector_server.embeddings import generate_embedding
   embedding = generate_embedding("React hooks")
   print(f"Embedding shape: {embedding.shape}")
   print(f"Embedding norm: {np.linalg.norm(embedding)}")
   ```

3. **Check database content**:
   ```python
   from src.mcp_vector_server.database import get_database_stats
   stats = get_database_stats()
   print(f"Total chunks: {stats['total_chunks']}")
   print(f"Technologies: {stats['technologies']}")
   ```

4. **Debug search process**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   
   results = search_documentation("React hooks")
   # Check debug logs for issues
   ```

#### Issue: `Embedding model download fails`

**Symptoms**:
```bash
OSError: Unable to load model from sentence-transformers/all-MiniLM-L6-v2
```

**Solutions**:
```bash
# Manual model download
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print('Model downloaded successfully')
"

# Check internet connection
curl -I https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

# Use offline mode (if model already downloaded)
export TRANSFORMERS_OFFLINE=1
```

### MCP Protocol Issues

#### Issue: MCP server doesn't respond

**Symptoms**:
```bash
$ echo '{"method": "tools/list"}' | uv run mcp-vector-server
# No response or hangs
```

**Debugging**:

1. **Enable debug mode**:
   ```bash
   export MCP_DEBUG=true
   export LOG_LEVEL=DEBUG
   uv run mcp-vector-server
   ```

2. **Check for startup errors**:
   ```bash
   uv run mcp-vector-server 2>&1 | grep -i error
   ```

3. **Test with simple request**:
   ```bash
   echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run mcp-vector-server
   ```

4. **Verify JSON format**:
   ```bash
   # Use proper JSON-RPC format
   cat << 'EOF' | uv run mcp-vector-server
   {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
   EOF
   ```

#### Issue: Invalid MCP responses

**Symptoms**:
```bash
# Malformed JSON or missing fields in responses
```

**Solutions**:
```python
# Validate response format
import json

response = '{"result": {...}}'  # Server response
try:
    parsed = json.loads(response)
    assert "jsonrpc" in parsed or "result" in parsed
    print("✅ Valid response format")
except (json.JSONDecodeError, AssertionError) as e:
    print(f"❌ Invalid response: {e}")
```

### Performance Issues

#### Issue: Slow search responses (>1 second)

**Symptoms**:
```bash
# Search takes several seconds to complete
```

**Debugging**:

1. **Profile search performance**:
   ```python
   import time
   
   start = time.time()
   results = search_documentation("test query")
   duration = time.time() - start
   print(f"Search took: {duration:.3f}s")
   ```

2. **Check system resources**:
   ```bash
   # Monitor during search
   top -p $(pgrep -f mcp-vector-server)
   
   # Check memory usage
   ps aux | grep mcp-vector-server
   ```

3. **Optimize query**:
   ```python
   # Use more specific queries
   results = search_documentation(
       "React useEffect hook cleanup", 
       technology="React",
       category="guides"
   )
   ```

4. **Check database size**:
   ```bash
   du -sh $VECTOR_DB_PATH
   # Large databases (>1GB) may be slow on first load
   ```

#### Issue: High memory usage

**Symptoms**:
```bash
# Process uses excessive RAM (>2GB)
```

**Solutions**:
```python
# Monitor memory usage
import tracemalloc

tracemalloc.start()
results = search_documentation("query")
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.1f} MB")
tracemalloc.stop()
```

```bash
# Reduce batch sizes
export EMBEDDING_BATCH_SIZE=100
export MAX_SEARCH_RESULTS=50
```

### IDE Integration Issues

#### Issue: Claude Code doesn't recognize MCP server

**Symptoms**:
- MCP server not listed in available tools
- Connection errors in Claude Code

**Solutions**:

1. **Verify MCP configuration**:
   ```json
   // ~/.claude/settings.json
   {
     "mcpServers": {
       "vector-search": {
         "command": "uv",
         "args": ["run", "mcp-vector-server"],
         "cwd": "/path/to/mcp-vector-server",
         "env": {
           "VECTOR_DB_PATH": "/path/to/vector/database"
         }
       }
     }
   }
   ```

2. **Test server manually**:
   ```bash
   cd /path/to/mcp-vector-server
   echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run mcp-vector-server
   ```

3. **Check logs**:
   ```bash
   # Claude Code logs location varies by OS
   tail -f ~/.claude/logs/mcp-server.log
   ```

#### Issue: VS Code MCP extension problems

**Symptoms**:
- MCP tools not available in VS Code
- Extension errors

**Solutions**:
```json
// .vscode/settings.json
{
  "mcp.servers": [
    {
      "name": "vector-search",
      "command": "uv",
      "args": ["run", "mcp-vector-server"],
      "cwd": "${workspaceFolder}/mcp-vector-server"
    }
  ]
}
```

### Development Environment Issues

#### Issue: Tests failing unexpectedly

**Symptoms**:
```bash
$ uv run pytest
FAILED tests/test_search.py::test_basic_search
```

**Debugging**:

1. **Run single test with verbose output**:
   ```bash
   uv run pytest -vvv -s tests/test_search.py::test_basic_search
   ```

2. **Check test dependencies**:
   ```bash
   uv sync --dev
   uv run pytest --collect-only  # Verify test discovery
   ```

3. **Reset test environment**:
   ```bash
   rm -rf .pytest_cache/
   uv run pytest tests/ --cache-clear
   ```

4. **Use debugging**:
   ```python
   # Add to failing test
   def test_basic_search():
       result = search_documentation("test")
       breakpoint()  # Interactive debugging
       assert len(result) > 0
   ```

#### Issue: Code formatting/linting failures

**Symptoms**:
```bash
$ uv run black --check src/
would reformat src/models.py
```

**Solutions**:
```bash
# Auto-fix formatting
uv run black src/ tests/
uv run isort src/ tests/

# Check specific issues
uv run black --diff src/models.py
uv run mypy src/models.py

# Fix all quality issues
uv run python scripts/fix_code_quality.py
```

## Debugging Tools & Techniques

### Logging Configuration

```python
# Enable comprehensive logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Search-specific logging
search_logger = logging.getLogger('mcp_vector_server.search')
search_logger.setLevel(logging.DEBUG)
```

### Interactive Debugging

```python
# Add breakpoints for investigation
def debug_search_issue():
    query = "problematic query"
    
    # Debug embedding generation
    embedding = generate_embedding(query)
    breakpoint()  # Investigate embedding
    
    # Debug similarity calculation
    similarities = calculate_similarities(embedding, db_embeddings)
    breakpoint()  # Check similarity scores
    
    # Debug result filtering
    filtered_results = apply_filters(similarities, filters)
    breakpoint()  # Verify filtering logic
```

### Performance Profiling

```bash
# Profile specific functions
uv run python -m cProfile -o profile.stats scripts/profile_search.py

# Analyze profile results
uv run python -c "
import pstats
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative').print_stats(20)
"

# Memory profiling
uv run python -m memory_profiler scripts/memory_test.py
```

### Network Debugging

```bash
# Test model download connectivity
curl -I https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

# Test with proxy (if needed)
export HTTPS_PROXY=http://proxy.company.com:8080
curl -I https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

# Check DNS resolution
nslookup huggingface.co
```

## Environment-Specific Issues

### macOS Issues

```bash
# Xcode command line tools (for some dependencies)
xcode-select --install

# Homebrew Python issues
brew install python@3.11
export PATH="/opt/homebrew/bin:$PATH"

# Permission issues with UV
sudo chown -R $(whoami) ~/.local/bin
```

### Linux Issues

```bash
# Missing system dependencies
sudo apt-get update
sudo apt-get install python3-dev build-essential

# For CentOS/RHEL
sudo yum install python3-devel gcc

# GPU support (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Windows/WSL Issues

```powershell
# WSL Python path issues
which python3
export PATH="/usr/bin:$PATH"

# Windows line ending issues
git config --global core.autocrlf input
```

## Getting Help

### Self-Diagnosis Checklist

Before seeking help, run through this checklist:

- [ ] Virtual environment activated (`source .venv/bin/activate`)
- [ ] Dependencies installed (`uv sync --dev`)
- [ ] Environment variables set (`echo $VECTOR_DB_PATH`)
- [ ] Database accessible (`ls -la $VECTOR_DB_PATH`)
- [ ] Basic imports work (`python -c "import mcp_vector_server"`)
- [ ] Minimal test passes (`uv run pytest tests/test_models.py -v`)

### Collecting Debug Information

When reporting issues, include:

```bash
# System information
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "UV: $(uv --version)"
echo "Working directory: $(pwd)"

# Environment
env | grep -E "(VECTOR_DB_PATH|MCP_|LOG_LEVEL)"

# Package versions
uv run pip freeze | grep -E "(mcp|sentence-transformers|numpy|pydantic)"

# Error logs
uv run mcp-vector-server 2>&1 | head -50
```

### Support Channels

1. **Documentation**: Check [Development Setup](./setup.md) and [API Reference](../api/reference.md)
2. **GitHub Issues**: Search existing issues or create new one
3. **GitHub Discussions**: Community support and questions
4. **Error Logs**: Always include full error messages and stack traces

### Issue Template

```markdown
## Bug Report

**Environment**:
- OS: [e.g., macOS 14.0, Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- UV version: [e.g., 0.1.35]
- Package version: [e.g., 0.1.0]

**Expected Behavior**:
[What you expected to happen]

**Actual Behavior**:
[What actually happened]

**Steps to Reproduce**:
1. [First step]
2. [Second step]
3. [And so on...]

**Error Messages**:
```
[Paste full error message and stack trace]
```

**Configuration**:
```bash
# Environment variables
echo $VECTOR_DB_PATH
# Any relevant config files
```

**Additional Context**:
[Any other context about the problem]
```

---

*Most issues can be resolved quickly with proper debugging techniques!* 🔧