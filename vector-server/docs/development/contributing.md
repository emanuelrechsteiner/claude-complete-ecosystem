# Contributing Guide

Welcome to the MCP Vector Server project! This guide will help you contribute effectively and maintain our high-quality codebase.

## 🚀 Quick Contribution Flow

1. **Fork & Clone**: Fork the repo and clone locally
2. **Setup**: Follow [Development Setup](./setup.md)
3. **Branch**: Create feature branch from `main`
4. **Develop**: Write code following our standards
5. **Test**: Ensure all tests pass
6. **Submit**: Open a pull request with clear description

## Development Standards

### Code Style

We maintain consistent code quality through automated tools:

```bash
# Format code (required before commit)
uv run black src/ tests/
uv run isort src/ tests/

# Type checking (must pass)
uv run mypy src/

# Quality verification
uv run python -m scripts.quality_check
```

#### Black Configuration
- Line length: 88 characters
- Target Python: 3.10+
- Skip string normalization: No

#### Import Sorting (isort)
- Profile: black compatibility
- Multi-line output mode: 3
- Force grid wrap: 0

### Type Hints

**Required**: All functions must have comprehensive type hints.

```python
# ✅ Good
def search_documents(
    query: str, 
    limit: int = 10,
    filters: Optional[Dict[str, Any]] = None
) -> List[SearchResult]:
    """Search documentation with optional filtering."""
    pass

# ❌ Bad
def search_documents(query, limit=10, filters=None):
    pass
```

### Documentation Standards

#### Docstring Format

Use Google-style docstrings for all public functions:

```python
def semantic_search(
    query: str,
    min_similarity: float = 0.3,
    technology: Optional[str] = None
) -> List[SearchResult]:
    """Perform semantic search across documentation chunks.
    
    Args:
        query: Natural language search query
        min_similarity: Minimum cosine similarity threshold (0.0-1.0)
        technology: Optional technology filter (e.g., "React", "Convex")
    
    Returns:
        List of search results ordered by relevance score
        
    Raises:
        ValueError: If min_similarity is outside valid range
        DatabaseError: If vector database is unavailable
        
    Example:
        >>> results = semantic_search("authentication in Convex", 0.5, "Convex")
        >>> print(f"Found {len(results)} relevant chunks")
    """
```

#### Code Comments

```python
# ✅ Good: Explain why, not what
# Normalize similarity scores to 0-1 range for consistent ranking
normalized_scores = (scores - min_score) / (max_score - min_score)

# ❌ Bad: States the obvious
# Loop through the results
for result in results:
```

### Error Handling

#### Exception Hierarchy

```python
class VectorServerError(Exception):
    """Base exception for all vector server errors."""
    pass

class DatabaseError(VectorServerError):
    """Database connection or query errors."""
    pass

class ValidationError(VectorServerError):
    """Input validation errors."""
    pass

class EmbeddingError(VectorServerError):
    """Embedding generation errors."""
    pass
```

#### Error Context

Always provide actionable error messages:

```python
# ✅ Good
raise ValidationError(
    f"Invalid similarity threshold: {similarity}. "
    f"Must be between 0.0 and 1.0"
)

# ❌ Bad
raise ValueError("Invalid input")
```

### Performance Guidelines

#### Vector Operations

```python
# ✅ Good: Vectorized operations
similarities = np.dot(query_embedding, doc_embeddings.T)

# ❌ Bad: Element-wise loops
similarities = [
    np.dot(query_embedding, doc_embedding) 
    for doc_embedding in doc_embeddings
]
```

#### Memory Management

```python
# ✅ Good: Generator for large datasets
def iter_chunks(batch_size: int = 1000) -> Iterator[List[DocumentChunk]]:
    for i in range(0, total_chunks, batch_size):
        yield load_chunk_batch(i, batch_size)

# ❌ Bad: Loading all into memory
def get_all_chunks() -> List[DocumentChunk]:
    return load_all_chunks()  # Could be 45K+ items
```

## Git Workflow

### Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/description` | `feature/add-category-filtering` |
| Bug fix | `fix/description` | `fix/similarity-threshold-validation` |
| Documentation | `docs/description` | `docs/api-reference-update` |
| Refactor | `refactor/description` | `refactor/search-engine-optimization` |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: type(scope): description
feat(search): add category-based filtering
fix(api): handle empty query validation
docs(setup): update installation requirements
refactor(models): optimize chunk serialization
test(search): add semantic similarity tests
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Pull Request Process

#### Before Submitting

```bash
# 1. Ensure code quality
uv run black src/ tests/
uv run isort src/ tests/
uv run mypy src/

# 2. Run all tests
uv run pytest --cov=src/mcp_vector_server

# 3. Check documentation
uv run python scripts/validate_docs.py

# 4. Verify integration
uv run python scripts/integration_test.py
```

#### PR Template

Use this template for pull requests:

```markdown
## Summary
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] All existing tests pass
- [ ] New tests added for changes
- [ ] Manual testing completed
- [ ] Integration tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or marked as such)

## Related Issues
Fixes #123
```

#### Review Criteria

PRs must meet these requirements:
- [ ] **Code Quality**: Follows style guide, proper type hints
- [ ] **Testing**: Adequate test coverage (>90%)
- [ ] **Documentation**: Updated relevant docs
- [ ] **Performance**: No significant performance regression
- [ ] **Security**: No security vulnerabilities introduced

## Testing Standards

### Test Categories

#### Unit Tests
```python
import pytest
from src.mcp_vector_server.models import SearchQuery, ValidationError

def test_search_query_validation():
    """Test SearchQuery input validation."""
    # Valid query
    query = SearchQuery(query="test", limit=5)
    assert query.limit == 5
    
    # Invalid limit
    with pytest.raises(ValidationError):
        SearchQuery(query="test", limit=101)
```

#### Integration Tests
```python
def test_search_integration(vector_database):
    """Test full search workflow."""
    results = search_documentation(
        query="React hooks tutorial",
        limit=3,
        technology="React"
    )
    
    assert len(results) <= 3
    assert all(r.similarity > 0.3 for r in results)
    assert results[0].similarity >= results[1].similarity
```

#### Performance Tests
```python
import time

def test_search_performance():
    """Ensure search completes within SLA."""
    start_time = time.time()
    
    results = search_documentation("complex query about authentication")
    
    elapsed = time.time() - start_time
    assert elapsed < 1.0  # Sub-second requirement
    assert len(results) > 0
```

### Test Data Management

#### Fixtures
```python
@pytest.fixture
def sample_chunks():
    """Sample documentation chunks for testing."""
    return [
        DocumentChunk(
            chunk_id="test_001",
            content="React hooks allow state management",
            metadata=ChunkMetadata(
                type="text",
                category="guides",
                doc_title="React Hooks Guide"
            )
        )
    ]
```

#### Mocking External Dependencies
```python
from unittest.mock import patch, MagicMock

@patch('src.mcp_vector_server.embeddings.SentenceTransformer')
def test_embedding_generation(mock_transformer):
    """Test embedding generation with mocked model."""
    mock_model = MagicMock()
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])
    mock_transformer.return_value = mock_model
    
    embedding = generate_embedding("test query")
    assert embedding.shape == (3,)
```

## Code Review Guidelines

### As a Reviewer

#### Focus Areas
1. **Correctness**: Does the code do what it claims?
2. **Performance**: Any obvious performance issues?
3. **Security**: Any security vulnerabilities?
4. **Maintainability**: Is the code readable and maintainable?
5. **Testing**: Are there adequate tests?

#### Feedback Style
```markdown
# ✅ Good feedback
Consider using a generator here to reduce memory usage for large datasets:
```python
def process_chunks():
    for chunk in iter_chunks():  # Generator
        yield process(chunk)
```

# ❌ Poor feedback
This is wrong, use generators.
```

### As a Contributor

#### Responding to Feedback
- **Be receptive**: Reviews help improve code quality
- **Ask questions**: If feedback is unclear, ask for clarification
- **Explain decisions**: Justify your approach if you disagree
- **Make changes promptly**: Address feedback in a timely manner

## Documentation Contributions

### API Documentation

Update API docs when adding new endpoints:

```python
def new_search_endpoint(
    query: str,
    filters: SearchFilters
) -> SearchResponse:
    """New search endpoint with advanced filtering.
    
    This endpoint extends the basic search with additional filtering
    capabilities for improved precision.
    
    Args:
        query: Natural language search query
        filters: Advanced filtering options
    
    Returns:
        Search response with ranked results
        
    Example:
        ```python
        response = new_search_endpoint(
            "authentication setup",
            SearchFilters(technology="Clerk", category="guides")
        )
        ```
    """
```

### User Documentation

Update user-facing docs in `/docs/` directory:
- API changes → Update [API Reference](../api/reference.md)
- New features → Update [Overview](../index.md)
- Setup changes → Update [Development Setup](./setup.md)

## Performance Benchmarking

### Adding Benchmarks

```python
# benchmarks/test_search_performance.py
import pytest
import time
from src.mcp_vector_server.search import search_documentation

@pytest.mark.benchmark
def test_search_latency(benchmark):
    """Benchmark search query latency."""
    result = benchmark(
        search_documentation,
        query="React hooks best practices",
        limit=10
    )
    assert len(result) > 0

@pytest.mark.benchmark
def test_memory_usage():
    """Monitor memory usage during search."""
    import tracemalloc
    
    tracemalloc.start()
    results = search_documentation("complex query")
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Ensure memory usage stays reasonable
    assert peak < 100 * 1024 * 1024  # 100MB limit
```

### Running Benchmarks

```bash
# Run performance benchmarks
uv run pytest -m benchmark --benchmark-only

# Profile specific functions
uv run python -m cProfile -o profile.stats scripts/profile_search.py

# Memory profiling
uv run python -m memory_profiler scripts/memory_test.py
```

## Security Guidelines

### Input Validation

Always validate and sanitize inputs:

```python
def validate_search_query(query: str) -> str:
    """Validate and sanitize search query."""
    if not query or not query.strip():
        raise ValidationError("Query cannot be empty")
    
    if len(query) > 1000:
        raise ValidationError("Query too long (max 1000 characters)")
    
    # Remove potential injection patterns
    sanitized = query.strip()
    
    return sanitized
```

### Dependency Security

```bash
# Check for security vulnerabilities
uv run safety check

# Update dependencies
uv sync --upgrade

# Audit specific packages
uv run pip-audit
```

## Release Process

### Version Management

Use semantic versioning (semver):
- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes

### Release Checklist

1. **Code Freeze**: No new features after code freeze
2. **Testing**: Full test suite passes
3. **Documentation**: All docs updated
4. **Performance**: Benchmarks meet SLA
5. **Security**: Security scan passes
6. **Review**: Code review complete

### Deployment

```bash
# Build release
uv build

# Tag release
git tag v1.2.3
git push origin v1.2.3

# Deploy to staging
python scripts/deploy_staging.py

# Deploy to production (after validation)
python scripts/deploy_production.py
```

## Getting Help

### Development Support

- **Setup Issues**: Check [Development Setup](./setup.md)
- **Testing Help**: See [Testing Guide](./testing.md)
- **Performance**: Review [Troubleshooting](./troubleshooting.md)

### Community

- **GitHub Discussions**: Feature discussions and questions
- **GitHub Issues**: Bug reports and feature requests
- **Code Review**: PR feedback and discussions

## Recognition

Contributors are recognized through:
- **GitHub Contributors**: Automatic recognition
- **Release Notes**: Major contributions highlighted
- **Documentation**: Contributor acknowledgments

---

Thank you for contributing to MCP Vector Server! 🎉