"""
Pytest configuration and fixtures for MCP Vector Server tests.

This module provides common test fixtures, configuration, and utilities
for the comprehensive test suite.
"""

import pytest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch
from typing import Dict, Any, List

# Import test utilities
from tests import clear_test_data, SAMPLE_OBSERVATION, SAMPLE_METRIC, SAMPLE_PATTERN

# Import server components
from mcp_vector_server.simple_server import (
    AGENT_OBSERVATIONS,
    AGENT_METRICS,
    COORDINATION_PATTERNS,
    store_agent_observation,
    store_agent_metric,
    analyze_coordination_patterns
)


@pytest.fixture(autouse=True)
def clear_data():
    """Automatically clear test data before and after each test."""
    clear_test_data()
    yield
    clear_test_data()


@pytest.fixture
def mock_vector_database():
    """Provide a mock vector database with test data."""
    mock_data = [
        {
            "chunk_id": "test_doc_1",
            "content": "React hooks documentation for functional components with state management",
            "metadata": {
                "type": "text",
                "category": "guides",
                "doc_title": "React Hooks Guide",
                "complexity": 0.6,
                "source_url": "https://react.dev/hooks"
            },
            "tokens": 12
        },
        {
            "chunk_id": "test_doc_2",
            "content": "Claude Code MCP protocol setup and configuration guide for developers",
            "metadata": {
                "type": "text",
                "category": "setup",
                "doc_title": "Claude Code Setup",
                "complexity": 0.7,
                "source_url": "https://claude.ai/code/setup"
            },
            "tokens": 11
        },
        {
            "chunk_id": "test_doc_3",
            "content": "TypeScript type definitions and interfaces for React component development",
            "metadata": {
                "type": "code",
                "category": "api_reference",
                "doc_title": "TypeScript Types",
                "complexity": 0.8,
                "source_url": "https://typescript.org/docs"
            },
            "tokens": 10
        },
        {
            "chunk_id": "test_doc_4",
            "content": "Performance optimization techniques for web applications including caching strategies",
            "metadata": {
                "type": "text", 
                "category": "guides",
                "doc_title": "Performance Guide",
                "complexity": 0.9,
                "source_url": "https://web.dev/performance"
            },
            "tokens": 13
        }
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        index_file = Path(temp_dir) / "vector_db_index.json"
        with open(index_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch.dict(os.environ, {'VECTOR_DB_PATH': temp_dir}):
            yield mock_data


@pytest.fixture
def sample_observations():
    """Provide sample agent observations for testing."""
    observations = []
    agent_types = ["backend-agent", "frontend-agent", "testing-agent"]
    categories = ["performance", "quality", "success", "improvement"]
    
    for i in range(12):  # 3 agent types * 4 categories
        agent_type = agent_types[i % len(agent_types)]
        category = categories[i % len(categories)]
        
        obs_id = store_agent_observation(
            agent_type=agent_type,
            task_id=f"sample_task_{i:03d}",
            project_id=f"sample_project_{i % 3}",  # 3 different projects
            category=category,
            content=f"Sample {category} observation {i} for {agent_type} testing and validation",
            observation_data={
                "index": i,
                "execution_time": 1.0 + (i * 0.1),
                "quality_score": 0.8 + (i % 20) * 0.01,
                "test_data": True
            },
            analysis={
                "performance_rating": 0.7 + (i % 30) * 0.01,
                "improvement_potential": 0.1 + (i % 10) * 0.02,
                "agent_efficiency": 0.85 + (i % 15) * 0.01
            },
            recommendations=[
                f"Recommendation {i % 5 + 1} for {agent_type}",
                f"Optimization suggestion {i % 3 + 1}"
            ],
            complexity=["low", "medium", "high", "critical"][i % 4],
            feature=f"feature_{i % 6}",
            environment=["development", "staging", "production"][i % 3]
        )
        observations.append(obs_id)
    
    return observations


@pytest.fixture
def sample_metrics():
    """Provide sample agent metrics for testing."""
    metrics = []
    agent_types = ["backend-agent", "frontend-agent", "testing-agent", "control-agent"]
    metric_types = ["response_time", "task_completion_rate", "quality_score", "coordination_efficiency"]
    
    for i, agent_type in enumerate(agent_types):
        metric_type = metric_types[i]
        
        # Generate 24 hours of measurements
        measurements = []
        for hour in range(24):
            measurements.append({
                "timestamp": f"2024-01-01T{hour:02d}:00:00",
                "value": 0.5 + (hour % 10) * 0.05 + (i * 0.1),
                "context": f"hour_{hour}",
                "agent_context": agent_type
            })
        
        metric_id = store_agent_metric(
            agent_type=agent_type,
            metric_type=metric_type,
            project_id=f"metrics_project_{i}",
            measurements=measurements,
            thresholds={
                "excellent": 0.2 + (i * 0.1),
                "good": 0.5 + (i * 0.1),
                "acceptable": 1.0 + (i * 0.1),
                "poor": 2.0 + (i * 0.1)
            },
            aggregation_period=["hour", "day"][i % 2]
        )
        metrics.append(metric_id)
    
    return metrics


@pytest.fixture 
def sample_coordination_patterns():
    """Provide sample coordination patterns for testing."""
    patterns = []
    
    pattern_configs = [
        {
            "name": "Sequential Backend-Frontend",
            "sequence": ["planning-agent", "backend-agent", "frontend-agent", "testing-agent"],
            "complexity": ["medium", "high"],
            "success_rate": 0.92
        },
        {
            "name": "Parallel Research Implementation",
            "sequence": ["control-agent", "research-agent", "backend-agent"],
            "complexity": ["high", "critical"],
            "success_rate": 0.88
        },
        {
            "name": "Documentation-Heavy Workflow",
            "sequence": ["planning-agent", "backend-agent", "documentation-agent", "testing-agent"],
            "complexity": ["low", "medium"],
            "success_rate": 0.95
        },
        {
            "name": "Rapid Prototyping Pattern",
            "sequence": ["frontend-agent", "testing-agent"],
            "complexity": ["low"],
            "success_rate": 0.85
        }
    ]
    
    for i, config in enumerate(pattern_configs):
        result = analyze_coordination_patterns(
            agent_sequence=config["sequence"],
            pattern_name=config["name"],
            project_context=f"pattern_project_{i}",
            success_metrics={
                "completion_rate": config["success_rate"],
                "time_efficiency": 0.8 + (i * 0.05),
                "quality_score": 0.85 + (i * 0.03),
                "coordination_overhead": 0.1 + (i * 0.02)
            },
            applicable_scenarios=[
                f"Scenario {j + 1} for {config['name']}" 
                for j in range(3)
            ],
            complexity_suitability=config["complexity"],
            historical_performance=[
                {
                    "date": f"2024-01-{day:02d}",
                    "success": True if day % 10 != 0 else False,
                    "duration": 3.0 + (day * 0.1) + (i * 0.5),
                    "quality": 0.8 + (day % 20) * 0.01
                }
                for day in range(1, 16)  # 15 historical executions
            ]
        )
        patterns.append(result["pattern_id"])
    
    return patterns


@pytest.fixture
def comprehensive_test_data(sample_observations, sample_metrics, sample_coordination_patterns):
    """Provide comprehensive test data combining all types."""
    return {
        "observations": sample_observations,
        "metrics": sample_metrics,
        "patterns": sample_coordination_patterns,
        "total_observations": len(AGENT_OBSERVATIONS),
        "total_metrics": len(AGENT_METRICS),
        "total_patterns": len(COORDINATION_PATTERNS)
    }


@pytest.fixture
def mcp_request_factory():
    """Factory for creating MCP request objects."""
    def create_request(method: str, params: Dict[str, Any] = None, request_id: int = 1):
        """Create a properly formatted MCP request."""
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        
        if params:
            request["params"] = params
        
        return request
    
    return create_request


@pytest.fixture
def mcp_tool_call_factory():
    """Factory for creating MCP tool call requests."""
    def create_tool_call(tool_name: str, arguments: Dict[str, Any], request_id: int = 1):
        """Create a properly formatted MCP tool call request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
    
    return create_tool_call


@pytest.fixture
def performance_timer():
    """Provide a performance timer utility."""
    import time
    import gc
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            gc.collect()  # Clean up before timing
            self.start_time = time.perf_counter()
        
        def stop(self):
            self.end_time = time.perf_counter()
            return self.elapsed
        
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
        
        def __enter__(self):
            self.start()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.stop()
    
    return Timer


@pytest.fixture
def memory_profiler():
    """Provide a memory profiler utility."""
    import psutil
    import gc
    
    class MemoryProfiler:
        def __init__(self):
            self.process = psutil.Process()
            self.initial_memory = None
            self.peak_memory = None
        
        def start(self):
            gc.collect()
            self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            self.peak_memory = self.initial_memory
        
        def update_peak(self):
            current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            self.peak_memory = max(self.peak_memory, current_memory)
            return current_memory
        
        def get_delta(self):
            current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            return current_memory - self.initial_memory if self.initial_memory else 0
    
    return MemoryProfiler


# Test markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests for end-to-end workflows") 
    config.addinivalue_line("markers", "performance: Performance and benchmarking tests")
    config.addinivalue_line("markers", "slow: Tests that take longer to execute")
    config.addinivalue_line("markers", "memory: Tests that analyze memory usage")
    config.addinivalue_line("markers", "concurrent: Tests that involve concurrent operations")


# Custom assertion helpers
def assert_mcp_response(response: Dict[str, Any], expected_id: int = None):
    """Assert that response follows MCP JSON-RPC 2.0 format."""
    assert "jsonrpc" in response, "Response missing jsonrpc field"
    assert response["jsonrpc"] == "2.0", f"Invalid jsonrpc version: {response['jsonrpc']}"
    
    if expected_id is not None:
        assert "id" in response, "Response missing id field"
        assert response["id"] == expected_id, f"Response ID {response['id']} doesn't match expected {expected_id}"
    
    # Should have either result or error, not both
    has_result = "result" in response
    has_error = "error" in response
    assert has_result != has_error, "Response must have either result or error, not both"


def assert_observation_structure(observation: Dict[str, Any]):
    """Assert that observation follows expected structure."""
    required_fields = ["chunk_id", "content", "metadata", "observation_data", "analysis"]
    for field in required_fields:
        assert field in observation, f"Observation missing required field: {field}"
    
    # Verify metadata structure
    metadata = observation["metadata"]
    required_metadata = ["type", "agent_type", "task_id", "project_id", "category", "timestamp"]
    for field in required_metadata:
        assert field in metadata, f"Observation metadata missing required field: {field}"
    
    assert metadata["type"] == "observation", f"Invalid metadata type: {metadata['type']}"


def assert_performance_within_threshold(elapsed_time: float, threshold: float, operation: str):
    """Assert that operation performance is within acceptable threshold."""
    assert elapsed_time <= threshold, f"{operation} took {elapsed_time:.4f}s, exceeds threshold of {threshold:.3f}s"