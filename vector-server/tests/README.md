# MCP Vector Server Agent Observation System - Test Suite

This directory contains a comprehensive test suite for the MCP Vector Server Agent Observation System, validating all new functionality for agent behavior tracking and performance monitoring.

## Test Coverage

### 📋 Test Modules

1. **`test_models.py`** - Data Model Validation
   - Tests all 9 new Pydantic models for type safety
   - Validates data serialization/deserialization
   - Tests model validation rules and constraints
   - Ensures backward compatibility with existing models

2. **`test_mcp_tools.py`** - MCP Tool Functionality
   - Tests all 5 new MCP tools for functionality
   - Validates JSON-RPC 2.0 protocol compliance  
   - Tests error handling and edge cases
   - Verifies tool schema definitions

3. **`test_integration.py`** - Integration Testing
   - Tests integration with existing vector database
   - Validates observation storage and retrieval workflows
   - Tests semantic search functionality with agent observations
   - Verifies cross-project data isolation

4. **`test_performance.py`** - Performance Validation
   - Benchmarks response times for all new tools
   - Validates sub-second response time requirements
   - Tests with realistic data volumes
   - Memory usage and resource consumption analysis

### 🔧 Test Configuration

- **`conftest.py`** - Pytest fixtures and configuration
- **`__init__.py`** - Test utilities and constants
- **`README.md`** - This documentation file

## New MCP Tools Tested

1. **`store_agent_observation`** - Store agent behavior observations
2. **`search_agent_observations`** - Search agent observations with filters
3. **`store_agent_metric`** - Store agent performance metrics
4. **`analyze_coordination_patterns`** - Analyze agent coordination patterns
5. **`generate_agent_insights`** - Generate insights from observations and metrics

## Data Models Tested

### Agent Observation Models
1. **`ObservationMetadata`** - Metadata for agent observations
2. **`AgentObservationChunk`** - Complete observation data structure
3. **`PerformanceMetricMetadata`** - Metadata for performance metrics
4. **`PerformanceMetricChunk`** - Complete metric data structure
5. **`CoordinationPatternMetadata`** - Metadata for coordination patterns
6. **`CoordinationPatternChunk`** - Complete pattern data structure

### Query and Result Models
7. **`AgentObservationQuery`** - Query parameters for observation search
8. **`AgentMetricQuery`** - Query parameters for metric search
9. **`PatternAnalysisQuery`** - Query parameters for pattern analysis

Additional result models: `AgentObservationResult`, `AgentMetricResult`, `PatternAnalysisResult`

## Running Tests

### Quick Start
```bash
# Run all tests
python run_tests.py

# Run specific test category
python run_tests.py unit
python run_tests.py mcp
python run_tests.py integration  
python run_tests.py performance

# Run with verbose output
python run_tests.py all --verbose

# Generate coverage report
python run_tests.py coverage
```

### Advanced Usage
```bash
# Run specific test file
PYTHONPATH=src python -m pytest tests/test_models.py -v

# Run specific test class
PYTHONPATH=src python -m pytest tests/test_models.py::TestObservationMetadata -v

# Run specific test method
PYTHONPATH=src python -m pytest tests/test_models.py::TestObservationMetadata::test_valid_observation_metadata -v

# Run tests with coverage
PYTHONPATH=src python -m pytest tests/ --cov=mcp_vector_server --cov-report=html

# Run performance tests with output
PYTHONPATH=src python -m pytest tests/test_performance.py -v -s
```

## Performance Benchmarks

### Expected Performance Thresholds
- **Store Observation**: < 100ms (typical: ~1ms)
- **Search Observations**: < 500ms for 100+ observations (typical: ~50ms)
- **Store Metric**: < 200ms for 1000 measurements (typical: ~10ms)
- **Analyze Pattern**: < 150ms (typical: ~5ms)
- **Generate Insights**: < 1000ms for comprehensive analysis (typical: ~200ms)
- **Memory Usage**: < 50MB for standard operations
- **Concurrent Requests**: 50 requests in < 2 seconds

### Performance Test Categories
- **Response Time Validation**: Ensures sub-second response times
- **Memory Usage Analysis**: Validates reasonable memory consumption
- **Scalability Testing**: Tests performance with large datasets
- **Concurrent Access**: Validates performance under concurrent load
- **Resource Utilization**: CPU and memory usage monitoring

## Test Data and Scenarios

### Test Scenarios Covered
1. **Single Agent Workflows**: Individual agent observation and metric storage
2. **Multi-Agent Coordination**: Complex workflows with multiple agent types
3. **Error Recovery**: Error conditions and recovery patterns
4. **Long-Running Projects**: Extended development cycles with many observations
5. **Cross-Project Analysis**: Data isolation and cross-project insights
6. **Performance Edge Cases**: Large datasets and high-concurrency scenarios

### Sample Test Data
- **Agent Types**: backend-agent, frontend-agent, testing-agent, control-agent, etc.
- **Categories**: performance, quality, coordination, error, success, improvement
- **Complexity Levels**: low, medium, high, critical
- **Project Contexts**: Multiple realistic project scenarios
- **Time Ranges**: Historical data spanning weeks and months

## Quality Assurance

### Test Quality Metrics
- **Test Coverage**: Aiming for 90%+ coverage on new functionality
- **Edge Case Coverage**: Comprehensive edge case and error condition testing
- **Performance Validation**: All operations meet sub-second requirements
- **Integration Validation**: End-to-end workflow testing
- **Regression Prevention**: Baseline performance benchmarks

### Automated Quality Checks
- **Linting**: Code style and quality validation
- **Type Checking**: Static type analysis with mypy
- **Security**: Basic security validation for data handling
- **Documentation**: Test documentation completeness

## Continuous Testing

### Pre-Commit Testing
```bash
# Recommended pre-commit test
python run_tests.py unit && python run_tests.py mcp
```

### Full Validation
```bash
# Complete validation before deployment
python run_tests.py all && python run_tests.py coverage
```

### Performance Monitoring
```bash
# Regular performance benchmarking
python run_tests.py performance --verbose
```

## Troubleshooting

### Common Issues

#### Import Errors
- Ensure `PYTHONPATH=src` is set when running pytest directly
- Use the provided `run_tests.py` script for automated path setup

#### Test Dependencies
- Install required dependencies: `pip install pytest pytest-cov psutil`
- Or use: `python run_tests.py install-deps`

#### Performance Test Failures
- Performance thresholds may vary by hardware
- Tests will warn for slow performance but only fail on critical issues
- Adjust thresholds in `tests/__init__.py` if needed for your environment

#### Memory Usage
- Large test datasets may consume significant memory
- Tests include memory cleanup and garbage collection
- Monitor system resources during performance tests

### Test Environment Setup
```bash
# Verify environment
python run_tests.py --help

# Check test setup
python -c "import mcp_vector_server; print('✅ Module import successful')"

# Validate test dependencies
python -c "import pytest, psutil; print('✅ Test dependencies available')"
```

## Contributing to Tests

### Adding New Tests
1. Follow existing test structure and naming conventions
2. Include both positive and negative test cases
3. Add performance benchmarks for new functionality
4. Update this README with new test descriptions

### Test Writing Guidelines
- Use descriptive test names that explain what is being tested
- Include comprehensive docstrings for test methods
- Test both success paths and error conditions
- Validate performance characteristics for new operations
- Ensure tests are deterministic and don't depend on external state

### Performance Test Guidelines
- Establish baseline benchmarks for new operations
- Test with realistic data volumes
- Include memory usage validation
- Test concurrent access scenarios
- Document expected performance characteristics

---

This test suite ensures the reliability, performance, and correctness of the MCP Vector Server Agent Observation System, providing confidence for production deployment and ongoing development.