"""
Test suite for MCP Vector Server Agent Observation System.

This package contains comprehensive tests for:
- Data model validation and integrity (test_models.py)
- MCP tool functionality and JSON-RPC compliance (test_mcp_tools.py)
- Integration testing with vector database (test_integration.py)
- Performance benchmarking and validation (test_performance.py)

Test Categories:
- Unit Tests: Individual component testing
- Integration Tests: End-to-end workflow testing
- Performance Tests: Response time and resource usage validation
- Regression Tests: Ensure no performance degradation

Usage:
    # Run all tests
    pytest tests/
    
    # Run specific test module
    pytest tests/test_models.py
    
    # Run with verbose output
    pytest tests/ -v
    
    # Run performance tests only
    pytest tests/test_performance.py -v -s
    
    # Generate coverage report
    pytest tests/ --cov=mcp_vector_server --cov-report=html
"""

__version__ = "1.0.0"
__author__ = "Claude Code Agent System"

# Test configuration constants
TEST_PROJECT_ID = "test_project_agent_observations"
TEST_AGENT_TYPE = "test-agent"
TEST_TASK_PREFIX = "test_task"

# Performance benchmark thresholds
PERFORMANCE_THRESHOLDS = {
    "store_observation_max_time": 0.1,      # 100ms
    "search_observations_max_time": 0.5,    # 500ms
    "store_metric_max_time": 0.2,           # 200ms
    "analyze_pattern_max_time": 0.15,       # 150ms
    "generate_insights_max_time": 1.0,      # 1 second
    "memory_usage_max_mb": 50.0,            # 50MB
    "concurrent_requests_max_time": 2.0     # 2 seconds for 50 requests
}

# Test data templates
SAMPLE_OBSERVATION = {
    "agent_type": "test-agent",
    "task_id": "test_task_001",
    "project_id": "test_project",
    "category": "performance",
    "content": "Sample test observation for validation",
    "observation_data": {
        "execution_time": 1.23,
        "memory_usage": 45.6,
        "test_coverage": 0.95
    },
    "analysis": {
        "performance_score": 0.87,
        "quality_indicators": ["high_coverage", "efficient_execution"],
        "bottlenecks": ["database_query_time"]
    },
    "recommendations": [
        "Optimize database query performance",
        "Implement caching for frequently accessed data"
    ]
}

SAMPLE_METRIC = {
    "agent_type": "test-agent",
    "metric_type": "response_time",
    "project_id": "test_project",
    "measurements": [
        {"timestamp": "2024-01-01T10:00:00", "value": 0.5},
        {"timestamp": "2024-01-01T11:00:00", "value": 0.7},
        {"timestamp": "2024-01-01T12:00:00", "value": 0.6}
    ],
    "thresholds": {
        "excellent": 0.3,
        "good": 0.7,
        "acceptable": 1.0
    }
}

SAMPLE_PATTERN = {
    "agent_sequence": ["planning-agent", "backend-agent", "testing-agent"],
    "pattern_name": "Sequential Development Pattern",
    "project_context": "test_project",
    "success_metrics": {
        "completion_rate": 0.92,
        "time_efficiency": 0.85,
        "quality_score": 0.90
    },
    "applicable_scenarios": [
        "Small to medium feature development",
        "Backend-heavy implementations",
        "Quality-critical projects"
    ]
}

# Test utilities
def clear_test_data():
    """Clear all test data from global storage."""
    from mcp_vector_server.simple_server import AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
    AGENT_OBSERVATIONS.clear()
    AGENT_METRICS.clear()
    COORDINATION_PATTERNS.clear()

def create_test_observation(index: int = 0, **overrides):
    """Create a test observation with optional overrides."""
    observation = SAMPLE_OBSERVATION.copy()
    observation["task_id"] = f"{TEST_TASK_PREFIX}_{index:03d}"
    observation["content"] = f"Test observation {index} - {observation['content']}"
    observation["observation_data"]["index"] = index
    
    for key, value in overrides.items():
        observation[key] = value
    
    return observation

def create_test_metric(agent_type: str = None, **overrides):
    """Create a test metric with optional overrides."""
    metric = SAMPLE_METRIC.copy()
    if agent_type:
        metric["agent_type"] = agent_type
    
    for key, value in overrides.items():
        metric[key] = value
    
    return metric

def create_test_pattern(pattern_name: str = None, **overrides):
    """Create a test coordination pattern with optional overrides."""
    pattern = SAMPLE_PATTERN.copy()
    if pattern_name:
        pattern["pattern_name"] = pattern_name
    
    for key, value in overrides.items():
        pattern[key] = value
    
    return pattern