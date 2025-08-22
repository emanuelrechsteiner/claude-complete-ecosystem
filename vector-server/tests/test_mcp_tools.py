#!/usr/bin/env python3
"""
Comprehensive test suite for MCP tool functionality.

This module tests all 5 new MCP tools for:
- JSON-RPC 2.0 compliance
- Tool functionality and error handling
- Schema validation
- Edge cases and performance
"""

import pytest
import json
import uuid
from datetime import datetime
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List

# Import the server functions to test
from mcp_vector_server.simple_server import (
    handle_request,
    search_documentation,
    store_agent_observation,
    search_agent_observations,
    store_agent_metric,
    analyze_coordination_patterns,
    generate_agent_insights,
    get_database,
    AGENT_OBSERVATIONS,
    AGENT_METRICS,
    COORDINATION_PATTERNS
)


class TestMCPProtocolCompliance:
    """Test JSON-RPC 2.0 protocol compliance for all MCP tools."""
    
    def test_initialize_request(self):
        """Test MCP initialize request compliance."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert response["result"]["protocolVersion"] == "2024-11-05"
        assert "capabilities" in response["result"]
        assert "serverInfo" in response["result"]
        assert response["result"]["serverInfo"]["name"] == "vector-search"
    
    def test_initialized_notification(self):
        """Test handling of initialized notification."""
        request = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        }
        
        response = handle_request(request)
        
        # Initialized is a notification, should return None
        assert response is None
    
    def test_tools_list_request(self):
        """Test tools/list request returns all expected tools."""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]
        
        tools = response["result"]["tools"]
        tool_names = [tool["name"] for tool in tools]
        
        expected_tools = [
            "search_documentation",
            "store_agent_observation",
            "search_agent_observations",
            "store_agent_metric",
            "analyze_coordination_patterns",
            "generate_agent_insights"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
        
        # Verify tool schemas are properly defined
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
            assert tool["inputSchema"]["type"] == "object"
            assert "properties" in tool["inputSchema"]
    
    def test_invalid_method_error(self):
        """Test proper error response for invalid method."""
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "invalid_method"
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert "error" in response
        assert response["error"]["code"] == -32601
        assert "Method not found" in response["error"]["message"]
    
    def test_parse_error_handling(self):
        """Test handling of malformed JSON requests."""
        # This would typically be handled at the transport layer,
        # but we test the response format
        request = {}  # Missing required fields
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert "error" in response
        assert response["error"]["code"] == -32603  # Internal error


class TestSearchDocumentationTool:
    """Test the search_documentation MCP tool."""
    
    def test_search_documentation_basic(self):
        """Test basic search documentation functionality."""
        request = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "search_documentation",
                "arguments": {
                    "query": "React hooks",
                    "limit": 5
                }
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 10
        assert "result" in response
        assert "content" in response["result"]
        assert len(response["result"]["content"]) == 1
        assert response["result"]["content"][0]["type"] == "text"
        
        # Parse the returned JSON content
        content_data = json.loads(response["result"]["content"][0]["text"])
        assert "results" in content_data
        assert isinstance(content_data["results"], list)
    
    def test_search_documentation_with_filters(self):
        """Test search with additional filters."""
        # First, need to populate database with test data
        with patch('mcp_vector_server.simple_server.get_database') as mock_db:
            mock_db.return_value = [
                {
                    "chunk_id": "test_1", 
                    "content": "React hooks tutorial guide", 
                    "category": "guides",
                    "metadata": {"type": "text", "category": "guides"}
                },
                {
                    "chunk_id": "test_2", 
                    "content": "Vue.js components documentation", 
                    "category": "api_reference",
                    "metadata": {"type": "text", "category": "api_reference"}
                }
            ]
            
            result = search_documentation("React hooks", limit=10)
            
            assert "results" in result
            assert len(result["results"]) >= 1
            
            # Verify results contain expected data
            first_result = result["results"][0]
            assert "chunk" in first_result
            assert "similarity" in first_result
            assert "rank" in first_result
            assert first_result["chunk"]["chunk_id"] == "test_1"
    
    def test_search_documentation_empty_query(self):
        """Test search with empty query."""
        result = search_documentation("", limit=10)
        
        assert "results" in result
        # Empty query should return no results or minimal results
        assert len(result["results"]) == 0
    
    def test_search_documentation_no_matches(self):
        """Test search with query that has no matches."""
        result = search_documentation("nonexistent_unique_term_12345", limit=10)
        
        assert "results" in result
        assert len(result["results"]) == 0


class TestAgentObservationTools:
    """Test agent observation storage and search tools."""
    
    def setUp(self):
        """Clear observation data before each test."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
    
    def test_store_agent_observation_valid(self):
        """Test storing a valid agent observation."""
        self.setUp()
        
        observation_id = store_agent_observation(
            agent_type="backend-agent",
            task_id="task_123",
            project_id="project_abc",
            category="performance",
            content="Successfully implemented user authentication API with JWT tokens",
            observation_data={
                "execution_time": 2.3,
                "memory_usage": 45.2,
                "test_coverage": 0.95
            },
            analysis={
                "performance_score": 0.87,
                "quality_indicators": ["high_coverage", "secure_implementation"],
                "bottlenecks": ["password_hashing"]
            },
            recommendations=["Consider bcrypt optimization for password hashing"],
            complexity="medium",
            feature="user-auth",
            environment="development"
        )
        
        assert observation_id.startswith("obs_")
        assert len(observation_id) == 12  # "obs_" + 8 hex chars
        
        # Verify observation was stored
        assert len(AGENT_OBSERVATIONS) == 1
        stored_obs = AGENT_OBSERVATIONS[0]
        
        assert stored_obs["chunk_id"] == observation_id
        assert stored_obs["metadata"]["agent_type"] == "backend-agent"
        assert stored_obs["metadata"]["task_id"] == "task_123"
        assert stored_obs["metadata"]["category"] == "performance"
        assert stored_obs["observation_data"]["execution_time"] == 2.3
        assert len(stored_obs["recommendations"]) == 1
    
    def test_store_agent_observation_via_mcp(self):
        """Test storing agent observation via MCP tool call."""
        self.setUp()
        
        request = {
            "jsonrpc": "2.0",
            "id": 20,
            "method": "tools/call",
            "params": {
                "name": "store_agent_observation",
                "arguments": {
                    "agent_type": "frontend-agent",
                    "task_id": "ui_task_456",
                    "project_id": "ecommerce_app",
                    "category": "quality",
                    "content": "Implemented responsive design with 98% accessibility compliance",
                    "observation_data": {
                        "render_time": 0.8,
                        "accessibility_score": 0.98,
                        "lighthouse_score": 92
                    },
                    "analysis": {
                        "user_experience": "excellent",
                        "performance": "good",
                        "accessibility": "excellent"
                    },
                    "recommendations": [
                        "Optimize image loading for better performance",
                        "Add keyboard navigation for dropdown menus"
                    ],
                    "complexity": "high"
                }
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 20
        assert "result" in response
        
        # Parse the response content
        content_data = json.loads(response["result"]["content"][0]["text"])
        assert "observation_id" in content_data
        assert "status" in content_data
        assert content_data["status"] == "stored"
        assert content_data["observation_id"].startswith("obs_")
    
    def test_search_agent_observations_basic(self):
        """Test basic agent observation search."""
        self.setUp()
        
        # Store test observation
        obs_id = store_agent_observation(
            agent_type="testing-agent",
            task_id="test_task_789",
            project_id="test_project",
            category="success",
            content="Unit test suite completed with 100% pass rate and 95% coverage",
            observation_data={"test_count": 42, "pass_rate": 1.0, "coverage": 0.95},
            analysis={"quality": "excellent", "confidence": "high"}
        )
        
        # Search for the observation
        results = search_agent_observations("unit test coverage", limit=10)
        
        assert "results" in results
        assert len(results["results"]) == 1
        
        result = results["results"][0]
        assert result["chunk"]["chunk_id"] == obs_id
        assert "similarity" in result
        assert "rank" in result
        assert result["rank"] == 1
    
    def test_search_agent_observations_with_filters(self):
        """Test agent observation search with filters."""
        self.setUp()
        
        # Store multiple observations
        obs1_id = store_agent_observation(
            agent_type="backend-agent",
            task_id="task_1",
            project_id="project_a",
            category="performance",
            content="Database query optimization completed",
            observation_data={"query_time": 0.5},
            analysis={"improvement": "significant"}
        )
        
        obs2_id = store_agent_observation(
            agent_type="frontend-agent",
            task_id="task_2",
            project_id="project_a",
            category="quality",
            content="UI component performance optimization",
            observation_data={"render_time": 0.3},
            analysis={"improvement": "moderate"}
        )
        
        # Search with agent_type filter
        results = search_agent_observations(
            query="optimization",
            limit=10,
            agent_type="backend-agent"
        )
        
        assert len(results["results"]) == 1
        assert results["results"][0]["chunk"]["chunk_id"] == obs1_id
        
        # Search with project filter
        results = search_agent_observations(
            query="optimization",
            limit=10,
            project_id="project_a"
        )
        
        assert len(results["results"]) == 2


class TestAgentMetricTools:
    """Test agent metric storage and retrieval tools."""
    
    def setUp(self):
        """Clear metric data before each test."""
        global AGENT_METRICS
        AGENT_METRICS.clear()
    
    def test_store_agent_metric_valid(self):
        """Test storing valid agent metrics."""
        self.setUp()
        
        measurements = [
            {"timestamp": "2024-01-01T09:00:00", "value": 1.2, "context": "morning"},
            {"timestamp": "2024-01-01T12:00:00", "value": 0.8, "context": "noon"},
            {"timestamp": "2024-01-01T15:00:00", "value": 1.1, "context": "afternoon"}
        ]
        
        metric_id = store_agent_metric(
            agent_type="backend-agent",
            metric_type="response_time",
            project_id="api_project",
            measurements=measurements,
            thresholds={"excellent": 0.5, "good": 1.0, "acceptable": 2.0},
            aggregation_period="hour"
        )
        
        assert metric_id.startswith("metric_")
        assert len(AGENT_METRICS) == 1
        
        stored_metric = AGENT_METRICS[0]
        assert stored_metric["chunk_id"] == metric_id
        assert stored_metric["metadata"]["agent_type"] == "backend-agent"
        assert stored_metric["metadata"]["metric_type"] == "response_time"
        assert len(stored_metric["measurements"]) == 3
        assert "statistics" in stored_metric
        assert stored_metric["statistics"]["mean"] == (1.2 + 0.8 + 1.1) / 3
    
    def test_store_agent_metric_via_mcp(self):
        """Test storing agent metric via MCP tool call."""
        self.setUp()
        
        request = {
            "jsonrpc": "2.0",
            "id": 30,
            "method": "tools/call",
            "params": {
                "name": "store_agent_metric",
                "arguments": {
                    "agent_type": "control-agent",
                    "metric_type": "coordination_efficiency",
                    "project_id": "multi_agent_project",
                    "measurements": [
                        {"timestamp": "2024-01-01T10:00:00", "value": 0.92, "agents": 4},
                        {"timestamp": "2024-01-01T11:00:00", "value": 0.87, "agents": 3},
                        {"timestamp": "2024-01-01T12:00:00", "value": 0.95, "agents": 5}
                    ],
                    "thresholds": {
                        "excellent": 0.9,
                        "good": 0.8,
                        "acceptable": 0.7
                    },
                    "aggregation_period": "hour"
                }
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 30
        assert "result" in response
        
        content_data = json.loads(response["result"]["content"][0]["text"])
        assert "metric_id" in content_data
        assert "status" in content_data
        assert content_data["status"] == "stored"


class TestCoordinationPatternTools:
    """Test coordination pattern analysis tools."""
    
    def setUp(self):
        """Clear pattern data before each test."""
        global COORDINATION_PATTERNS
        COORDINATION_PATTERNS.clear()
    
    def test_analyze_coordination_patterns_valid(self):
        """Test analyzing valid coordination patterns."""
        self.setUp()
        
        result = analyze_coordination_patterns(
            agent_sequence=["control-agent", "planning-agent", "backend-agent", "frontend-agent", "testing-agent"],
            pattern_name="Full Stack Sequential",
            project_context="e-commerce-platform",
            success_metrics={
                "completion_rate": 0.91,
                "time_efficiency": 0.85,
                "quality_score": 0.93
            },
            applicable_scenarios=[
                "New feature development",
                "Full application implementation",
                "Complex integration projects"
            ],
            complexity_suitability=["medium", "high", "critical"]
        )
        
        assert "pattern_id" in result
        assert "effectiveness_score" in result
        assert "optimization_suggestions" in result
        assert result["effectiveness_score"] == 0.91
        
        # Verify pattern was stored
        assert len(COORDINATION_PATTERNS) == 1
        stored_pattern = COORDINATION_PATTERNS[0]
        assert stored_pattern["metadata"]["pattern_name"] == "Full Stack Sequential"
        assert len(stored_pattern["metadata"]["agent_sequence"]) == 5
    
    def test_analyze_coordination_patterns_via_mcp(self):
        """Test coordination pattern analysis via MCP tool call."""
        self.setUp()
        
        request = {
            "jsonrpc": "2.0",
            "id": 40,
            "method": "tools/call",
            "params": {
                "name": "analyze_coordination_patterns",
                "arguments": {
                    "agent_sequence": ["research-agent", "backend-agent"],
                    "pattern_name": "Parallel Research Implementation",
                    "project_context": "ai_integration",
                    "success_metrics": {
                        "completion_rate": 0.88,
                        "time_efficiency": 0.92,
                        "coordination_overhead": 0.12
                    },
                    "applicable_scenarios": [
                        "Unknown API integration",
                        "New technology adoption"
                    ]
                }
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 40
        assert "result" in response
        
        content_data = json.loads(response["result"]["content"][0]["text"])
        assert "pattern_id" in content_data
        assert "effectiveness_score" in content_data
        assert content_data["effectiveness_score"] == 0.88


class TestInsightGenerationTool:
    """Test agent insight generation tool."""
    
    def setUp(self):
        """Set up test data for insight generation."""
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        COORDINATION_PATTERNS.clear()
        
        # Add test data
        store_agent_observation(
            agent_type="backend-agent",
            task_id="task_1",
            project_id="test_project",
            category="performance",
            content="API optimization completed",
            observation_data={"response_time": 0.5},
            analysis={"improvement": "significant"},
            recommendations=["Cache frequently accessed data", "Optimize database queries"]
        )
        
        store_agent_metric(
            agent_type="backend-agent",
            metric_type="response_time",
            project_id="test_project",
            measurements=[{"timestamp": "2024-01-01T12:00:00", "value": 0.5}]
        )
        
        analyze_coordination_patterns(
            agent_sequence=["backend-agent", "testing-agent"],
            pattern_name="Backend-Testing Sequential",
            project_context="test_project",
            success_metrics={"completion_rate": 0.95}
        )
    
    def test_generate_agent_insights_all_agents(self):
        """Test generating insights for all agents."""
        self.setUp()
        
        insights = generate_agent_insights()
        
        assert "summary" in insights
        assert "performance_trends" in insights
        assert "recommendations" in insights
        assert "patterns" in insights
        
        summary = insights["summary"]
        assert summary["total_observations"] == 1
        assert summary["total_metrics"] == 1
        assert summary["total_patterns"] == 1
        assert "backend-agent" in summary["agent_types"]
        
        # Should have recommendations from observations
        assert len(insights["recommendations"]) >= 1
        assert "Cache frequently accessed data" in insights["recommendations"]
        
        # Should have pattern information
        assert len(insights["patterns"]) >= 1
        pattern = insights["patterns"][0]
        assert "pattern_name" in pattern
        assert "effectiveness" in pattern
    
    def test_generate_agent_insights_specific_agent(self):
        """Test generating insights for specific agent type."""
        self.setUp()
        
        insights = generate_agent_insights(agent_type="backend-agent")
        
        assert insights["summary"]["total_observations"] == 1
        assert insights["summary"]["agent_types"] == ["backend-agent"]
    
    def test_generate_agent_insights_via_mcp(self):
        """Test generating insights via MCP tool call."""
        self.setUp()
        
        request = {
            "jsonrpc": "2.0",
            "id": 50,
            "method": "tools/call",
            "params": {
                "name": "generate_agent_insights",
                "arguments": {
                    "agent_type": "backend-agent"
                }
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 50
        assert "result" in response
        
        content_data = json.loads(response["result"]["content"][0]["text"])
        assert "summary" in content_data
        assert "recommendations" in content_data
        assert "patterns" in content_data


class TestErrorHandling:
    """Test error handling for all MCP tools."""
    
    def test_store_agent_observation_missing_required_field(self):
        """Test error handling for missing required fields."""
        request = {
            "jsonrpc": "2.0",
            "id": 60,
            "method": "tools/call",
            "params": {
                "name": "store_agent_observation",
                "arguments": {
                    "agent_type": "backend-agent",
                    # Missing task_id, project_id, category, content, observation_data, analysis
                }
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 60
        assert "error" in response
        assert response["error"]["code"] == -32603  # Internal error
    
    def test_search_agent_observations_invalid_limit(self):
        """Test search with invalid limit parameter."""
        # This would be caught by the schema validation in the actual MCP server
        # Here we test the function directly
        results = search_agent_observations("test", limit=0)
        
        # Function should handle gracefully
        assert "results" in results
    
    def test_malformed_json_request(self):
        """Test handling of malformed JSON in tool calls."""
        # Test with invalid JSON structure
        request = {
            "jsonrpc": "2.0",
            "id": 70,
            "method": "tools/call",
            "params": {
                "name": "invalid_tool_name",
                "arguments": {}
            }
        }
        
        response = handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 70
        assert "error" in response
        assert response["error"]["code"] == -32603


class TestPerformanceAndConcurrency:
    """Test performance characteristics and concurrent access."""
    
    def test_large_observation_data_handling(self):
        """Test handling of large observation data."""
        large_data = {f"metric_{i}": i * 0.1 for i in range(1000)}
        
        start_time = datetime.now()
        
        obs_id = store_agent_observation(
            agent_type="data-agent",
            task_id="large_task",
            project_id="big_data_project",
            category="performance",
            content="Processed large dataset with 1000 metrics",
            observation_data=large_data,
            analysis={"size": len(large_data), "processing_time": 2.5}
        )
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Should complete within reasonable time (< 1 second)
        assert processing_time < 1.0
        assert obs_id is not None
        assert len(AGENT_OBSERVATIONS) >= 1
    
    def test_concurrent_observation_storage(self):
        """Test concurrent storage of observations."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Simulate multiple concurrent observations
        observation_ids = []
        for i in range(10):
            obs_id = store_agent_observation(
                agent_type=f"agent-{i}",
                task_id=f"task_{i}",
                project_id="concurrent_test",
                category="performance",
                content=f"Concurrent observation {i}",
                observation_data={"index": i},
                analysis={"concurrent": True}
            )
            observation_ids.append(obs_id)
        
        # All observations should be stored
        assert len(AGENT_OBSERVATIONS) == 10
        assert len(set(observation_ids)) == 10  # All IDs should be unique
    
    def test_search_performance_with_many_observations(self):
        """Test search performance with many stored observations."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Store many observations
        for i in range(100):
            store_agent_observation(
                agent_type="performance-agent",
                task_id=f"perf_task_{i}",
                project_id="performance_project",
                category="performance",
                content=f"Performance test observation {i} with optimization data",
                observation_data={"iteration": i, "performance_score": 0.8 + (i % 20) * 0.01},
                analysis={"test_run": i}
            )
        
        start_time = datetime.now()
        
        results = search_agent_observations("optimization", limit=20)
        
        end_time = datetime.now()
        search_time = (end_time - start_time).total_seconds()
        
        # Search should complete quickly (< 0.5 seconds)
        assert search_time < 0.5
        assert len(results["results"]) >= 1
        assert len(results["results"]) <= 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])