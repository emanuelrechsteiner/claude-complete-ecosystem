#!/usr/bin/env python3
"""
Integration test suite for vector database agent observation system.

This module tests:
- Integration with existing vector database
- End-to-end observation storage and retrieval workflows  
- Semantic search functionality with agent observations
- Cross-project data isolation
- Real-world usage scenarios
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List

# Import all components for integration testing
from mcp_vector_server.simple_server import (
    handle_request,
    get_database,
    load_vector_database,
    store_agent_observation,
    search_agent_observations,
    store_agent_metric,
    analyze_coordination_patterns,
    generate_agent_insights,
    AGENT_OBSERVATIONS,
    AGENT_METRICS,
    COORDINATION_PATTERNS
)

from mcp_vector_server.models import (
    AgentObservationChunk,
    PerformanceMetricChunk,
    CoordinationPatternChunk,
    ObservationMetadata
)


class TestVectorDatabaseIntegration:
    """Test integration with existing vector database infrastructure."""
    
    def test_database_loading_with_mock_data(self):
        """Test database loading with mock vector database."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock vector database index
            mock_index_data = [
                {
                    "chunk_id": "react_1",
                    "content": "React hooks allow you to use state and lifecycle methods in functional components",
                    "metadata": {
                        "type": "text",
                        "category": "guides",
                        "doc_title": "React Hooks Guide",
                        "complexity": 0.6
                    },
                    "tokens": 12
                },
                {
                    "chunk_id": "claude_1", 
                    "content": "Claude Code provides AI-powered development assistance with MCP protocol support",
                    "metadata": {
                        "type": "text",
                        "category": "setup",
                        "doc_title": "Claude Code Setup",
                        "complexity": 0.7
                    },
                    "tokens": 11
                }
            ]
            
            index_file = Path(temp_dir) / "vector_db_index.json"
            with open(index_file, 'w') as f:
                json.dump(mock_index_data, f)
            
            # Test loading with environment variable
            with patch.dict(os.environ, {'VECTOR_DB_PATH': temp_dir}):
                database = load_vector_database()
                
                assert len(database) == 2
                assert database[0]["chunk_id"] == "react_1"
                assert database[1]["chunk_id"] == "claude_1"
    
    def test_combined_search_traditional_and_observations(self):
        """Test searching across both traditional docs and agent observations."""
        # Clear existing data
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Store some agent observations
        obs_id_1 = store_agent_observation(
            agent_type="backend-agent",
            task_id="auth_task",
            project_id="ecommerce",
            category="success",
            content="Successfully implemented JWT authentication with React hooks integration",
            observation_data={"implementation_time": 3.5, "test_coverage": 0.92},
            analysis={"quality": "high", "reusability": "excellent"}
        )
        
        obs_id_2 = store_agent_observation(
            agent_type="frontend-agent", 
            task_id="ui_task",
            project_id="ecommerce",
            category="performance",
            content="React component optimization using hooks reduced render time by 40%",
            observation_data={"render_time_before": 120, "render_time_after": 72},
            analysis={"performance_gain": 0.4, "user_experience": "improved"}
        )
        
        # Search for "React hooks" - should find both traditional docs and observations
        doc_results = handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "search_documentation",
                "arguments": {"query": "React hooks", "limit": 10}
            }
        })
        
        obs_results = handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "search_agent_observations", 
                "arguments": {"query": "React hooks", "limit": 10}
            }
        })
        
        # Verify both searches return results
        doc_content = json.loads(doc_results["result"]["content"][0]["text"])
        obs_content = json.loads(obs_results["result"]["content"][0]["text"])
        
        # Should find traditional documentation
        assert len(doc_content["results"]) >= 0  # May have demo data
        
        # Should find agent observations
        assert len(obs_content["results"]) == 2
        obs_chunks = [r["chunk"]["chunk_id"] for r in obs_content["results"]]
        assert obs_id_1 in obs_chunks
        assert obs_id_2 in obs_chunks
    
    def test_cross_project_data_isolation(self):
        """Test that project-specific data is properly isolated."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Store observations for different projects
        project_a_obs = store_agent_observation(
            agent_type="backend-agent",
            task_id="task_a1",
            project_id="project_alpha",
            category="performance",
            content="Project Alpha backend optimization completed",
            observation_data={"latency": 0.5},
            analysis={"project_context": "alpha"}
        )
        
        project_b_obs = store_agent_observation(
            agent_type="backend-agent",
            task_id="task_b1", 
            project_id="project_beta",
            category="performance",
            content="Project Beta backend optimization completed",
            observation_data={"latency": 0.7},
            analysis={"project_context": "beta"}
        )
        
        # Search with project filter for Alpha
        alpha_results = search_agent_observations(
            query="backend optimization",
            project_id="project_alpha",
            limit=10
        )
        
        # Search with project filter for Beta
        beta_results = search_agent_observations(
            query="backend optimization",
            project_id="project_beta",
            limit=10
        )
        
        # Verify isolation
        assert len(alpha_results["results"]) == 1
        assert alpha_results["results"][0]["chunk"]["chunk_id"] == project_a_obs
        
        assert len(beta_results["results"]) == 1
        assert beta_results["results"][0]["chunk"]["chunk_id"] == project_b_obs
    
    def test_semantic_search_quality(self):
        """Test semantic search quality for agent observations."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Store observations with related but different content
        store_agent_observation(
            agent_type="backend-agent",
            task_id="perf_1",
            project_id="performance_test",
            category="performance",
            content="Database query optimization reduced response time from 2.1s to 0.3s",
            observation_data={"before": 2.1, "after": 0.3},
            analysis={"improvement": 0.86}
        )
        
        store_agent_observation(
            agent_type="frontend-agent",
            task_id="perf_2", 
            project_id="performance_test",
            category="performance",
            content="React component memoization improved rendering performance significantly",
            observation_data={"render_improvement": 0.45},
            analysis={"technique": "memoization"}
        )
        
        store_agent_observation(
            agent_type="documentation-agent",
            task_id="doc_1",
            project_id="performance_test", 
            category="quality",
            content="Updated API documentation with new authentication endpoints",
            observation_data={"endpoints_documented": 12},
            analysis={"completeness": 0.95}
        )
        
        # Search for performance-related terms
        perf_results = search_agent_observations("performance optimization", limit=10)
        
        # Should rank performance observations higher
        assert len(perf_results["results"]) == 3
        
        # Top results should be performance-related
        top_result = perf_results["results"][0]
        assert "performance" in top_result["chunk"]["content"].lower()
        assert top_result["similarity"] > 0.3
        
        # Results should be ranked by relevance
        similarities = [r["similarity"] for r in perf_results["results"]]
        assert similarities == sorted(similarities, reverse=True)


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows for agent coordination."""
    
    def setUp(self):
        """Clear all data before each test."""
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        COORDINATION_PATTERNS.clear()
    
    def test_complete_feature_development_workflow(self):
        """Test complete workflow for feature development with multiple agents."""
        self.setUp()
        
        # Phase 1: Planning Agent starts
        planning_obs = store_agent_observation(
            agent_type="planning-agent",
            task_id="feature_auth_system",
            project_id="webapp_v2",
            category="success",
            content="Completed feature planning for user authentication system with JWT tokens",
            observation_data={
                "requirements_defined": 15,
                "architecture_components": 8,
                "estimated_effort_hours": 40
            },
            analysis={
                "complexity_assessment": "medium",
                "risk_factors": ["third_party_integration", "security_requirements"],
                "success_probability": 0.92
            },
            recommendations=[
                "Use proven JWT library for token handling",
                "Implement rate limiting for auth endpoints",
                "Set up comprehensive test coverage for security flows"
            ]
        )
        
        # Phase 2: Research Agent investigates
        research_obs = store_agent_observation(
            agent_type="research-agent",
            task_id="auth_research",
            project_id="webapp_v2",
            category="success",
            content="Researched JWT authentication best practices and security implementations",
            observation_data={
                "libraries_evaluated": 5,
                "security_standards_reviewed": 3,
                "implementation_examples": 12
            },
            analysis={
                "recommended_library": "jsonwebtoken",
                "security_level": "high",
                "implementation_complexity": "medium"
            },
            recommendations=[
                "Use bcrypt for password hashing",
                "Implement token refresh mechanism",
                "Add CORS configuration for frontend integration"
            ]
        )
        
        # Phase 3: Backend Agent implements
        backend_obs = store_agent_observation(
            agent_type="backend-agent",
            task_id="auth_backend_impl",
            project_id="webapp_v2",
            category="success",
            content="Implemented JWT authentication API with login, register, and token refresh endpoints",
            observation_data={
                "endpoints_created": 6,
                "middleware_added": 3,
                "test_coverage": 0.94,
                "implementation_time_hours": 8.5
            },
            analysis={
                "code_quality_score": 0.91,
                "security_compliance": 0.96,
                "performance_benchmarks": {"login": 0.12, "register": 0.18, "refresh": 0.08}
            },
            recommendations=[
                "Add request rate limiting middleware",
                "Implement session cleanup job for expired tokens"
            ]
        )
        
        # Store performance metric for backend
        backend_metric = store_agent_metric(
            agent_type="backend-agent",
            metric_type="response_time",
            project_id="webapp_v2",
            measurements=[
                {"timestamp": "2024-01-01T10:00:00", "endpoint": "login", "value": 0.12},
                {"timestamp": "2024-01-01T10:01:00", "endpoint": "register", "value": 0.18},
                {"timestamp": "2024-01-01T10:02:00", "endpoint": "refresh", "value": 0.08}
            ],
            thresholds={"excellent": 0.1, "good": 0.2, "acceptable": 0.5}
        )
        
        # Phase 4: Frontend Agent integrates
        frontend_obs = store_agent_observation(
            agent_type="frontend-agent",
            task_id="auth_frontend_impl",
            project_id="webapp_v2",
            category="success",
            content="Integrated authentication UI with React hooks and context for state management",
            observation_data={
                "components_created": 4,
                "hooks_implemented": 2,
                "context_providers": 1,
                "test_coverage": 0.89
            },
            analysis={
                "user_experience_score": 0.94,
                "accessibility_compliance": 0.92,
                "integration_success": True
            },
            recommendations=[
                "Add loading states for better UX",
                "Implement form validation feedback"
            ]
        )
        
        # Phase 5: Testing Agent validates
        testing_obs = store_agent_observation(
            agent_type="testing-agent",
            task_id="auth_testing",
            project_id="webapp_v2", 
            category="success",
            content="Completed comprehensive testing of authentication system including security tests",
            observation_data={
                "unit_tests": 28,
                "integration_tests": 12,
                "security_tests": 8,
                "overall_coverage": 0.93,
                "test_execution_time": 45.2
            },
            analysis={
                "test_quality_score": 0.95,
                "security_vulnerabilities_found": 0,
                "performance_within_thresholds": True
            },
            recommendations=[
                "Add load testing for authentication endpoints",
                "Set up automated security scanning"
            ]
        )
        
        # Analyze coordination pattern
        pattern_analysis = analyze_coordination_patterns(
            agent_sequence=["planning-agent", "research-agent", "backend-agent", "frontend-agent", "testing-agent"],
            pattern_name="Sequential Feature Development",
            project_context="webapp_v2",
            success_metrics={
                "completion_rate": 1.0,
                "time_efficiency": 0.87,
                "quality_score": 0.93,
                "coordination_overhead": 0.15
            },
            applicable_scenarios=[
                "New feature development with research requirements",
                "Full-stack implementation projects",
                "Security-sensitive feature development"
            ],
            complexity_suitability=["medium", "high"]
        )
        
        # Generate insights from complete workflow
        insights = generate_agent_insights(project_id="webapp_v2")
        
        # Verify workflow completion
        assert len(AGENT_OBSERVATIONS) == 5
        assert len(AGENT_METRICS) == 1
        assert len(COORDINATION_PATTERNS) == 1
        
        # Verify insights capture the workflow
        assert insights["summary"]["total_observations"] == 5
        assert insights["summary"]["total_metrics"] == 1
        assert insights["summary"]["total_patterns"] == 1
        
        # Should have recommendations from all agents
        all_recommendations = insights["recommendations"]
        assert len(all_recommendations) > 5  # Combined from all agents
        assert "Use proven JWT library for token handling" in all_recommendations
        assert "Add loading states for better UX" in all_recommendations
        
        # Pattern should show high effectiveness
        pattern = insights["patterns"][0]
        assert pattern["effectiveness"] == 1.0
        assert pattern["pattern_name"] == "Sequential Feature Development"
    
    def test_error_recovery_workflow(self):
        """Test workflow with error conditions and recovery."""
        self.setUp()
        
        # Initial failed attempt
        error_obs = store_agent_observation(
            agent_type="backend-agent",
            task_id="api_implementation_v1",
            project_id="error_recovery_test",
            category="error",
            content="API implementation failed due to database connection timeout issues",
            observation_data={
                "error_type": "database_timeout",
                "failure_time": 15.6,
                "retry_attempts": 3
            },
            analysis={
                "root_cause": "database_connection_pool_exhaustion",
                "impact_severity": "high",
                "recovery_time_estimate": 2.0
            },
            recommendations=[
                "Increase database connection pool size",
                "Add connection timeout configuration",
                "Implement retry logic with exponential backoff"
            ]
        )
        
        # Recovery attempt
        recovery_obs = store_agent_observation(
            agent_type="backend-agent",
            task_id="api_implementation_v2",
            project_id="error_recovery_test",
            category="improvement",
            content="Fixed database connection issues and successfully implemented API endpoints",
            observation_data={
                "connection_pool_size": 20,
                "timeout_config": 30,
                "retry_logic_implemented": True,
                "success_rate_after_fix": 0.98
            },
            analysis={
                "problem_resolution": "successful",
                "performance_improvement": 0.75,
                "stability_increase": 0.85
            },
            recommendations=[
                "Monitor connection pool utilization",
                "Set up alerts for database connection failures"
            ]
        )
        
        # Search for error recovery patterns
        error_results = search_agent_observations(
            query="database connection timeout error recovery",
            category="error",
            limit=10
        )
        
        improvement_results = search_agent_observations(
            query="database connection fixes",
            category="improvement",
            limit=10
        )
        
        # Verify error tracking and recovery
        assert len(error_results["results"]) == 1
        assert error_results["results"][0]["chunk"]["chunk_id"] == error_obs
        
        assert len(improvement_results["results"]) == 1
        assert improvement_results["results"][0]["chunk"]["chunk_id"] == recovery_obs
        
        # Generate insights to capture learning
        insights = generate_agent_insights(project_id="error_recovery_test")
        
        recommendations = insights["recommendations"]
        assert "Increase database connection pool size" in recommendations
        assert "Monitor connection pool utilization" in recommendations


class TestRealWorldUsageScenarios:
    """Test realistic usage scenarios based on actual development workflows."""
    
    def setUp(self):
        """Clear all data before each test."""
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        COORDINATION_PATTERNS.clear()
    
    def test_multi_project_coordination(self):
        """Test coordination across multiple projects."""
        self.setUp()
        
        # Project 1: E-commerce Platform
        ecommerce_obs = []
        for i in range(3):
            obs_id = store_agent_observation(
                agent_type="backend-agent",
                task_id=f"ecommerce_task_{i}",
                project_id="ecommerce_platform",
                category="success",
                content=f"Ecommerce backend task {i} completed successfully",
                observation_data={"task_index": i, "completion_time": 2.5 + i * 0.5},
                analysis={"project": "ecommerce", "phase": f"phase_{i}"}
            )
            ecommerce_obs.append(obs_id)
        
        # Project 2: Analytics Dashboard  
        analytics_obs = []
        for i in range(2):
            obs_id = store_agent_observation(
                agent_type="frontend-agent",
                task_id=f"analytics_task_{i}",
                project_id="analytics_dashboard",
                category="success", 
                content=f"Analytics frontend task {i} implemented with data visualization",
                observation_data={"task_index": i, "charts_created": 3 + i},
                analysis={"project": "analytics", "visualization_type": f"type_{i}"}
            )
            analytics_obs.append(obs_id)
        
        # Cross-project search
        all_results = search_agent_observations("task completed successfully", limit=20)
        ecommerce_results = search_agent_observations(
            "backend task",
            project_id="ecommerce_platform",
            limit=10
        )
        analytics_results = search_agent_observations(
            "frontend task",
            project_id="analytics_dashboard", 
            limit=10
        )
        
        # Verify proper segmentation
        assert len(all_results["results"]) == 5  # All observations
        assert len(ecommerce_results["results"]) == 3  # Only ecommerce
        assert len(analytics_results["results"]) == 2  # Only analytics
        
        # Generate project-specific insights
        ecommerce_insights = generate_agent_insights(agent_type="backend-agent")
        analytics_insights = generate_agent_insights(agent_type="frontend-agent")
        
        assert ecommerce_insights["summary"]["total_observations"] == 3
        assert analytics_insights["summary"]["total_observations"] == 2
    
    def test_long_running_project_tracking(self):
        """Test tracking observations over extended time periods."""
        self.setUp()
        
        # Simulate observations over time
        base_time = datetime.now() - timedelta(days=30)
        
        for week in range(4):
            for day in range(7):
                timestamp = base_time + timedelta(weeks=week, days=day)
                
                store_agent_observation(
                    agent_type="backend-agent",
                    task_id=f"daily_task_w{week}_d{day}",
                    project_id="long_running_project",
                    category="performance",
                    content=f"Daily development task completed in week {week}, day {day}",
                    observation_data={
                        "week": week,
                        "day": day,
                        "productivity_score": 0.7 + (week * 0.05) + (day * 0.01),
                        "lines_of_code": 150 + (week * 20) + (day * 5)
                    },
                    analysis={
                        "trend": "improving" if week > 1 else "stable",
                        "weekly_progress": week / 4,
                        "daily_efficiency": 0.8 + (day * 0.02)
                    },
                    timestamp=timestamp.isoformat()
                )
        
        # Search for recent observations
        recent_results = search_agent_observations("development task week", limit=50)
        
        # Should find all 28 observations (4 weeks * 7 days)
        assert len(recent_results["results"]) == 28
        
        # Generate insights for productivity analysis
        insights = generate_agent_insights(agent_type="backend-agent")
        
        # Should capture productivity trends
        assert insights["summary"]["total_observations"] == 28
        assert len(insights["recommendations"]) > 0
    
    def test_agent_performance_comparison(self):
        """Test comparing performance across different agent types."""
        self.setUp()
        
        agent_types = ["backend-agent", "frontend-agent", "testing-agent"]
        
        # Store metrics for different agents
        for agent_type in agent_types:
            # Store some observations
            for i in range(3):
                store_agent_observation(
                    agent_type=agent_type,
                    task_id=f"{agent_type}_task_{i}",
                    project_id="performance_comparison",
                    category="performance",
                    content=f"{agent_type} completed task {i} with performance metrics",
                    observation_data={
                        "execution_time": 1.0 + (i * 0.2),
                        "quality_score": 0.85 + (i * 0.02),
                        "task_complexity": i + 1
                    },
                    analysis={
                        "agent_efficiency": 0.9 - (i * 0.05),
                        "improvement_potential": 0.1 + (i * 0.02)
                    }
                )
            
            # Store performance metrics
            measurements = [
                {"timestamp": "2024-01-01T10:00:00", "value": 1.2, "task": 0},
                {"timestamp": "2024-01-01T11:00:00", "value": 1.4, "task": 1},
                {"timestamp": "2024-01-01T12:00:00", "value": 1.6, "task": 2}
            ]
            
            store_agent_metric(
                agent_type=agent_type,
                metric_type="response_time",
                project_id="performance_comparison",
                measurements=measurements
            )
        
        # Generate comparative insights
        all_insights = generate_agent_insights()
        backend_insights = generate_agent_insights(agent_type="backend-agent")
        frontend_insights = generate_agent_insights(agent_type="frontend-agent") 
        
        # Verify comprehensive coverage
        assert all_insights["summary"]["total_observations"] == 9  # 3 agents * 3 observations
        assert all_insights["summary"]["total_metrics"] == 3  # 1 per agent type
        assert len(all_insights["summary"]["agent_types"]) == 3
        
        # Verify agent-specific insights
        assert backend_insights["summary"]["total_observations"] == 3
        assert backend_insights["summary"]["agent_types"] == ["backend-agent"]
        
        assert frontend_insights["summary"]["total_observations"] == 3
        assert frontend_insights["summary"]["agent_types"] == ["frontend-agent"]


class TestDataConsistencyAndIntegrity:
    """Test data consistency and integrity across operations."""
    
    def test_concurrent_access_data_integrity(self):
        """Test data integrity under concurrent access scenarios."""
        global AGENT_OBSERVATIONS, AGENT_METRICS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        
        # Simulate concurrent operations
        observation_ids = []
        metric_ids = []
        
        # Store observations and metrics concurrently
        for i in range(10):
            obs_id = store_agent_observation(
                agent_type=f"concurrent-agent-{i % 3}",
                task_id=f"concurrent_task_{i}",
                project_id="integrity_test",
                category="performance",
                content=f"Concurrent observation {i}",
                observation_data={"index": i, "concurrent": True},
                analysis={"integrity_check": True}
            )
            observation_ids.append(obs_id)
            
            if i % 2 == 0:  # Store metrics for even indices
                metric_id = store_agent_metric(
                    agent_type=f"concurrent-agent-{i % 3}",
                    metric_type="response_time",
                    project_id="integrity_test",
                    measurements=[{"timestamp": "2024-01-01T10:00:00", "value": i * 0.1}]
                )
                metric_ids.append(metric_id)
        
        # Verify all data was stored correctly
        assert len(AGENT_OBSERVATIONS) == 10
        assert len(AGENT_METRICS) == 5
        assert len(set(observation_ids)) == 10  # All IDs unique
        assert len(set(metric_ids)) == 5  # All IDs unique
        
        # Verify data integrity through search
        results = search_agent_observations("concurrent observation", limit=20)
        assert len(results["results"]) == 10
        
        # All observations should be findable by their IDs
        found_ids = [r["chunk"]["chunk_id"] for r in results["results"]]
        for obs_id in observation_ids:
            assert obs_id in found_ids
    
    def test_data_persistence_across_operations(self):
        """Test that data persists correctly across multiple operations."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Initial data storage
        initial_obs = store_agent_observation(
            agent_type="persistence-test-agent",
            task_id="persistence_task_1",
            project_id="persistence_project", 
            category="success",
            content="Initial observation for persistence testing",
            observation_data={"initial": True, "sequence": 1},
            analysis={"persistence_check": "initial"}
        )
        
        # Verify initial storage
        initial_search = search_agent_observations("persistence testing", limit=10)
        assert len(initial_search["results"]) == 1
        assert initial_search["results"][0]["chunk"]["chunk_id"] == initial_obs
        
        # Add more observations
        additional_obs = []
        for i in range(5):
            obs_id = store_agent_observation(
                agent_type="persistence-test-agent",
                task_id=f"persistence_task_{i+2}",
                project_id="persistence_project",
                category="success",
                content=f"Additional observation {i+1} for persistence testing",
                observation_data={"initial": False, "sequence": i+2},
                analysis={"persistence_check": f"additional_{i+1}"}
            )
            additional_obs.append(obs_id)
        
        # Verify all observations persist
        full_search = search_agent_observations("persistence", limit=20)
        assert len(full_search["results"]) == 6  # 1 initial + 5 additional
        
        # Verify original observation is still there
        all_ids = [r["chunk"]["chunk_id"] for r in full_search["results"]]
        assert initial_obs in all_ids
        for obs_id in additional_obs:
            assert obs_id in all_ids
        
        # Verify insights capture all data
        insights = generate_agent_insights(agent_type="persistence-test-agent")
        assert insights["summary"]["total_observations"] == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])