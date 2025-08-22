#!/usr/bin/env python3
"""
Performance validation test suite for vector database agent observation system.

This module tests:
- Response time benchmarking for all MCP tools
- Sub-second response time validation
- Memory usage and resource consumption analysis
- Scalability testing with realistic data volumes
- Performance regression detection
"""

import pytest
import time
import psutil
import json
import gc
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import patch

# Import components for performance testing
from mcp_vector_server.simple_server import (
    handle_request,
    store_agent_observation,
    search_agent_observations,
    store_agent_metric,
    analyze_coordination_patterns,
    generate_agent_insights,
    search_documentation,
    AGENT_OBSERVATIONS,
    AGENT_METRICS,
    COORDINATION_PATTERNS
)


class PerformanceTimer:
    """Utility class for precise performance timing."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start timing."""
        gc.collect()  # Clean up before timing
        self.start_time = time.perf_counter()
    
    def stop(self):
        """Stop timing and return elapsed time."""
        self.end_time = time.perf_counter()
        return self.end_time - self.start_time
    
    @property
    def elapsed(self):
        """Get elapsed time."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class MemoryProfiler:
    """Utility class for memory usage profiling."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.initial_memory = None
        self.peak_memory = None
    
    def start_profiling(self):
        """Start memory profiling."""
        gc.collect()
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = self.initial_memory
    
    def update_peak(self):
        """Update peak memory usage."""
        current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = max(self.peak_memory, current_memory)
        return current_memory
    
    def get_memory_delta(self):
        """Get memory usage delta from start."""
        current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        return current_memory - self.initial_memory if self.initial_memory else 0


class TestMCPToolPerformance:
    """Performance tests for all MCP tools."""
    
    def setUp(self):
        """Clear data before each test."""
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        COORDINATION_PATTERNS.clear()
    
    def test_store_agent_observation_performance(self):
        """Test performance of storing agent observations."""
        self.setUp()
        
        timer = PerformanceTimer()
        memory_profiler = MemoryProfiler()
        
        # Performance test for single observation
        timer.start()
        memory_profiler.start_profiling()
        
        observation_id = store_agent_observation(
            agent_type="performance-test-agent",
            task_id="perf_task_001",
            project_id="performance_validation",
            category="performance",
            content="Performance test observation with comprehensive data structure including analysis and recommendations",
            observation_data={
                "execution_time": 1.234,
                "memory_usage": 45.67,
                "cpu_utilization": 0.78,
                "disk_io": {"read": 1024, "write": 512},
                "network_requests": 15,
                "cache_hits": 89,
                "cache_misses": 11,
                "database_queries": 8,
                "external_api_calls": 3,
                "error_count": 0
            },
            analysis={
                "performance_score": 0.89,
                "bottlenecks": ["database_query_optimization", "cache_miss_rate"],
                "optimization_opportunities": ["query_caching", "index_optimization", "connection_pooling"],
                "risk_assessment": {"level": "low", "factors": ["performance_degradation", "memory_leak"]},
                "quality_metrics": {
                    "code_coverage": 0.94,
                    "cyclomatic_complexity": 12,
                    "maintainability_index": 78
                }
            },
            recommendations=[
                "Implement query result caching for frequently accessed data",
                "Add database connection pooling to reduce connection overhead",
                "Optimize database indexes for better query performance",
                "Monitor memory usage patterns to prevent memory leaks"
            ],
            correlations=["obs_related_001", "obs_related_002", "pattern_cache_optimization"],
            complexity="high",
            feature="performance_optimization_engine",
            environment="production"
        )
        
        elapsed_time = timer.stop()
        memory_delta = memory_profiler.get_memory_delta()
        
        # Performance assertions
        assert elapsed_time < 0.1, f"Store operation took {elapsed_time:.4f}s, should be < 0.1s"
        assert memory_delta < 5.0, f"Memory usage increased by {memory_delta:.2f}MB, should be < 5MB"
        assert observation_id is not None
        assert len(AGENT_OBSERVATIONS) == 1
        
        print(f"Store observation performance: {elapsed_time:.4f}s, Memory: {memory_delta:.2f}MB")
    
    def test_search_agent_observations_performance(self):
        """Test performance of searching agent observations."""
        self.setUp()
        
        # Prepare test data - store multiple observations
        observation_ids = []
        for i in range(100):
            obs_id = store_agent_observation(
                agent_type=f"agent-{i % 5}",  # 5 different agent types
                task_id=f"task_{i:03d}",
                project_id=f"project_{i % 10}",  # 10 different projects
                category=["performance", "quality", "success", "improvement", "error"][i % 5],
                content=f"Search performance test observation {i} with detailed content about optimization and implementation details including database queries caching mechanisms and performance monitoring",
                observation_data={
                    "index": i,
                    "performance_metric": 0.5 + (i % 50) * 0.01,
                    "complexity_score": (i % 10) + 1,
                    "resource_usage": {"cpu": i % 100, "memory": (i % 200) + 100}
                },
                analysis={
                    "efficiency": 0.7 + (i % 30) * 0.01,
                    "quality_score": 0.8 + (i % 20) * 0.01,
                    "test_batch": i // 10
                }
            )
            observation_ids.append(obs_id)
        
        timer = PerformanceTimer()
        memory_profiler = MemoryProfiler()
        
        # Test search performance
        timer.start()
        memory_profiler.start_profiling()
        
        search_results = search_agent_observations(
            query="performance test observation optimization database",
            limit=20
        )
        
        elapsed_time = timer.stop()
        memory_delta = memory_profiler.get_memory_delta()
        
        # Performance assertions
        assert elapsed_time < 0.5, f"Search operation took {elapsed_time:.4f}s, should be < 0.5s"
        assert memory_delta < 10.0, f"Memory usage increased by {memory_delta:.2f}MB during search"
        assert len(search_results["results"]) <= 20
        assert len(search_results["results"]) > 0
        
        print(f"Search performance (100 observations): {elapsed_time:.4f}s, Memory: {memory_delta:.2f}MB")
        
        # Test filtered search performance
        timer.start()
        
        filtered_results = search_agent_observations(
            query="optimization",
            agent_type="agent-1",
            project_id="project_3",
            limit=10
        )
        
        filtered_elapsed = timer.stop()
        
        assert filtered_elapsed < 0.3, f"Filtered search took {filtered_elapsed:.4f}s, should be < 0.3s"
        
        print(f"Filtered search performance: {filtered_elapsed:.4f}s")
    
    def test_store_agent_metric_performance(self):
        """Test performance of storing agent metrics."""
        self.setUp()
        
        # Prepare large measurement dataset
        measurements = []
        for i in range(1000):  # 1000 measurements
            measurements.append({
                "timestamp": f"2024-01-01T{(i // 60) % 24:02d}:{i % 60:02d}:00",
                "value": 0.5 + (i % 100) * 0.01,
                "context": f"measurement_{i}",
                "metadata": {
                    "server_id": f"server_{i % 10}",
                    "region": f"region_{i % 5}",
                    "environment": "performance_test"
                }
            })
        
        timer = PerformanceTimer()
        memory_profiler = MemoryProfiler()
        
        timer.start()
        memory_profiler.start_profiling()
        
        metric_id = store_agent_metric(
            agent_type="performance-metric-agent",
            metric_type="response_time",
            project_id="metric_performance_test",
            measurements=measurements,
            thresholds={
                "excellent": 0.1,
                "good": 0.5,
                "acceptable": 1.0,
                "poor": 2.0
            },
            aggregation_period="minute"
        )
        
        elapsed_time = timer.stop()
        memory_delta = memory_profiler.get_memory_delta()
        
        # Performance assertions for large dataset
        assert elapsed_time < 0.2, f"Store metric operation took {elapsed_time:.4f}s, should be < 0.2s"
        assert memory_delta < 20.0, f"Memory usage increased by {memory_delta:.2f}MB for 1000 measurements"
        assert metric_id is not None
        assert len(AGENT_METRICS) == 1
        
        # Verify statistics calculation performance
        stored_metric = AGENT_METRICS[0]
        assert "statistics" in stored_metric
        assert stored_metric["statistics"]["count"] == 1000
        
        print(f"Store metric performance (1000 measurements): {elapsed_time:.4f}s, Memory: {memory_delta:.2f}MB")
    
    def test_analyze_coordination_patterns_performance(self):
        """Test performance of coordination pattern analysis."""
        self.setUp()
        
        # Prepare comprehensive pattern data
        agent_sequence = [
            "control-agent", "planning-agent", "research-agent", "backend-agent", 
            "frontend-agent", "testing-agent", "documentation-agent", "version-control-agent"
        ]
        
        success_metrics = {
            "completion_rate": 0.94,
            "time_efficiency": 0.87,
            "quality_score": 0.91,
            "coordination_overhead": 0.15,
            "resource_utilization": 0.83,
            "error_rate": 0.02,
            "communication_efficiency": 0.89
        }
        
        historical_performance = []
        for i in range(50):  # 50 historical executions
            historical_performance.append({
                "execution_id": f"exec_{i:03d}",
                "date": f"2024-01-{(i % 30) + 1:02d}",
                "success": i % 10 != 0,  # 90% success rate
                "duration": 4.5 + (i % 20) * 0.2,
                "quality_score": 0.8 + (i % 20) * 0.01,
                "resource_usage": {
                    "agent_hours": 8 + (i % 15),
                    "coordination_calls": 10 + (i % 8),
                    "handoff_count": len(agent_sequence) - 1
                }
            })
        
        timer = PerformanceTimer()
        memory_profiler = MemoryProfiler()
        
        timer.start()
        memory_profiler.start_profiling()
        
        analysis_result = analyze_coordination_patterns(
            agent_sequence=agent_sequence,
            pattern_name="Comprehensive Multi-Agent Sequential Pattern",
            project_context="large_scale_application_development",
            success_metrics=success_metrics,
            applicable_scenarios=[
                "Large-scale application development with comprehensive requirements",
                "Multi-team coordination for complex feature implementation",
                "Full-stack development with research and documentation requirements",
                "Quality-critical projects requiring extensive testing and validation",
                "Enterprise applications with strict documentation standards"
            ],
            complexity_suitability=["high", "critical"],
            historical_performance=historical_performance,
            optimizations=[
                {"type": "communication", "description": "Reduce check-in frequency to 45 minutes for stable agents"},
                {"type": "parallelization", "description": "Run documentation agent parallel with testing phase"},
                {"type": "resource_allocation", "description": "Allocate dedicated resources for coordination overhead"},
                {"type": "automation", "description": "Automate handoff validation between agents"}
            ]
        )
        
        elapsed_time = timer.stop()
        memory_delta = memory_profiler.get_memory_delta()
        
        # Performance assertions
        assert elapsed_time < 0.15, f"Pattern analysis took {elapsed_time:.4f}s, should be < 0.15s"
        assert memory_delta < 15.0, f"Memory usage increased by {memory_delta:.2f}MB during analysis"
        assert "pattern_id" in analysis_result
        assert "effectiveness_score" in analysis_result
        assert analysis_result["effectiveness_score"] == 0.94
        assert len(COORDINATION_PATTERNS) == 1
        
        print(f"Pattern analysis performance (8 agents, 50 history records): {elapsed_time:.4f}s, Memory: {memory_delta:.2f}MB")
    
    def test_generate_agent_insights_performance(self):
        """Test performance of generating comprehensive agent insights."""
        self.setUp()
        
        # Prepare comprehensive test dataset
        agent_types = ["control-agent", "backend-agent", "frontend-agent", "testing-agent", "documentation-agent"]
        
        # Store many observations
        for i in range(200):  # 200 observations
            store_agent_observation(
                agent_type=agent_types[i % len(agent_types)],
                task_id=f"insight_task_{i:03d}",
                project_id=f"insight_project_{i % 20}",  # 20 projects
                category=["performance", "quality", "success", "improvement", "error"][i % 5],
                content=f"Insight generation test observation {i} with comprehensive analysis data for performance benchmarking and quality assessment including detailed metrics and recommendations",
                observation_data={
                    "metric_index": i,
                    "performance_score": 0.6 + (i % 40) * 0.01,
                    "quality_metrics": {"coverage": 0.8 + (i % 20) * 0.01, "complexity": (i % 15) + 1}
                },
                analysis={
                    "efficiency_rating": 0.7 + (i % 30) * 0.01,
                    "improvement_potential": 0.1 + (i % 10) * 0.02,
                    "risk_level": ["low", "medium", "high"][i % 3]
                },
                recommendations=[
                    f"Recommendation {i % 10 + 1} for optimization",
                    f"Improvement suggestion {i % 15 + 1} for quality enhancement"
                ]
            )
        
        # Store metrics
        for agent_type in agent_types:
            measurements = [{"timestamp": f"2024-01-01T{i:02d}:00:00", "value": 0.5 + i * 0.1} for i in range(24)]
            store_agent_metric(
                agent_type=agent_type,
                metric_type="response_time", 
                project_id="insight_performance_test",
                measurements=measurements
            )
        
        # Store coordination patterns
        for i in range(10):  # 10 patterns
            analyze_coordination_patterns(
                agent_sequence=agent_types[:3 + (i % 3)],  # Variable sequence lengths
                pattern_name=f"Pattern {i}",
                project_context=f"pattern_project_{i}",
                success_metrics={"completion_rate": 0.8 + (i % 20) * 0.01}
            )
        
        timer = PerformanceTimer()
        memory_profiler = MemoryProfiler()
        
        # Test comprehensive insight generation
        timer.start()
        memory_profiler.start_profiling()
        
        all_insights = generate_agent_insights()
        
        elapsed_time = timer.stop()
        memory_delta = memory_profiler.get_memory_delta()
        
        # Performance assertions for large dataset
        assert elapsed_time < 1.0, f"Insight generation took {elapsed_time:.4f}s, should be < 1.0s"
        assert memory_delta < 25.0, f"Memory usage increased by {memory_delta:.2f}MB during insight generation"
        
        # Verify comprehensive results
        assert all_insights["summary"]["total_observations"] == 200
        assert all_insights["summary"]["total_metrics"] == 5
        assert all_insights["summary"]["total_patterns"] == 10
        assert len(all_insights["summary"]["agent_types"]) == 5
        assert len(all_insights["recommendations"]) > 0
        assert len(all_insights["patterns"]) > 0
        
        print(f"Comprehensive insight generation (200 obs, 5 metrics, 10 patterns): {elapsed_time:.4f}s, Memory: {memory_delta:.2f}MB")
        
        # Test agent-specific insight performance
        timer.start()
        
        specific_insights = generate_agent_insights(agent_type="backend-agent")
        
        specific_elapsed = timer.stop()
        
        assert specific_elapsed < 0.5, f"Agent-specific insights took {specific_elapsed:.4f}s, should be < 0.5s"
        assert specific_insights["summary"]["total_observations"] == 40  # 200 / 5 agent types
        
        print(f"Agent-specific insight generation: {specific_elapsed:.4f}s")


class TestMCPProtocolPerformance:
    """Performance tests for MCP protocol compliance and response times."""
    
    def test_mcp_request_handling_performance(self):
        """Test performance of MCP request handling."""
        timer = PerformanceTimer()
        
        # Test tools/list performance
        timer.start()
        
        tools_response = handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        
        tools_elapsed = timer.stop()
        
        assert tools_elapsed < 0.01, f"Tools list request took {tools_elapsed:.4f}s, should be < 0.01s"
        assert tools_response["jsonrpc"] == "2.0"
        assert "result" in tools_response
        
        print(f"MCP tools/list performance: {tools_elapsed:.4f}s")
        
        # Test tool call performance
        timer.start()
        
        tool_call_response = handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "store_agent_observation",
                "arguments": {
                    "agent_type": "performance-agent",
                    "task_id": "mcp_perf_task",
                    "project_id": "mcp_performance_test",
                    "category": "performance",
                    "content": "MCP protocol performance test observation",
                    "observation_data": {"response_time": 0.05},
                    "analysis": {"protocol_compliance": "excellent"}
                }
            }
        })
        
        tool_call_elapsed = timer.stop()
        
        assert tool_call_elapsed < 0.15, f"MCP tool call took {tool_call_elapsed:.4f}s, should be < 0.15s"
        assert tool_call_response["jsonrpc"] == "2.0"
        assert "result" in tool_call_response
        
        print(f"MCP tool call performance: {tool_call_elapsed:.4f}s")
    
    def test_concurrent_mcp_requests_performance(self):
        """Test performance under concurrent MCP requests."""
        import threading
        import queue
        
        results_queue = queue.Queue()
        request_count = 50
        
        def make_request(request_id):
            """Make a single MCP request."""
            timer = PerformanceTimer()
            timer.start()
            
            response = handle_request({
                "jsonrpc": "2.0",
                "id": request_id,
                "method": "tools/call",
                "params": {
                    "name": "search_agent_observations",
                    "arguments": {
                        "query": f"concurrent request {request_id}",
                        "limit": 5
                    }
                }
            })
            
            elapsed = timer.stop()
            results_queue.put((request_id, elapsed, response))
        
        # Clear data for consistent test
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Store test data
        for i in range(20):
            store_agent_observation(
                agent_type="concurrent-test-agent",
                task_id=f"concurrent_task_{i}",
                project_id="concurrent_test",
                category="performance",
                content=f"Concurrent request test data {i}",
                observation_data={"index": i},
                analysis={"concurrent_test": True}
            )
        
        # Launch concurrent requests
        start_time = time.perf_counter()
        threads = []
        
        for i in range(request_count):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all requests to complete
        for thread in threads:
            thread.join()
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Collect results
        response_times = []
        successful_responses = 0
        
        while not results_queue.empty():
            request_id, elapsed, response = results_queue.get()
            response_times.append(elapsed)
            if "result" in response:
                successful_responses += 1
        
        # Performance assertions
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        assert avg_response_time < 0.5, f"Average response time {avg_response_time:.4f}s too high"
        assert max_response_time < 1.0, f"Maximum response time {max_response_time:.4f}s too high"
        assert successful_responses == request_count, f"Only {successful_responses}/{request_count} requests succeeded"
        assert total_time < 10.0, f"Total concurrent execution time {total_time:.4f}s too high"
        
        print(f"Concurrent requests ({request_count}): Total={total_time:.4f}s, Avg={avg_response_time:.4f}s, Max={max_response_time:.4f}s")


class TestScalabilityAndResourceUsage:
    """Test scalability and resource usage characteristics."""
    
    def test_memory_usage_scalability(self):
        """Test memory usage scaling with data volume."""
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        COORDINATION_PATTERNS.clear()
        
        memory_profiler = MemoryProfiler()
        memory_profiler.start_profiling()
        
        data_points = [100, 500, 1000, 2000]
        memory_usage = []
        
        for count in data_points:
            # Clear previous data
            AGENT_OBSERVATIONS.clear()
            gc.collect()
            
            initial_memory = memory_profiler.update_peak()
            
            # Store observations
            for i in range(count):
                store_agent_observation(
                    agent_type=f"scalability-agent-{i % 10}",
                    task_id=f"scalability_task_{i}",
                    project_id=f"scalability_project_{i % 50}",
                    category=["performance", "quality", "success"][i % 3],
                    content=f"Scalability test observation {i} with comprehensive data for memory usage analysis and performance benchmarking including detailed metrics",
                    observation_data={
                        "index": i,
                        "batch": count,
                        "memory_test": True,
                        "complexity": (i % 20) + 1,
                        "metrics": [j * 0.1 for j in range(10)]  # Array data
                    },
                    analysis={
                        "scalability_test": True,
                        "memory_usage_expected": count * 0.001,  # Rough estimate
                        "data_size": len(str(i)) + 200  # Rough content size
                    }
                )
            
            final_memory = memory_profiler.update_peak()
            memory_delta = final_memory - initial_memory
            memory_usage.append((count, memory_delta))
            
            print(f"Memory usage for {count} observations: {memory_delta:.2f}MB")
        
        # Analyze memory scaling
        # Memory usage should scale roughly linearly
        small_ratio = memory_usage[1][1] / memory_usage[0][1]  # 500/100
        large_ratio = memory_usage[3][1] / memory_usage[2][1]  # 2000/1000
        
        # Memory usage should be reasonable and scale predictably
        assert memory_usage[0][1] < 50.0, f"Memory for 100 observations ({memory_usage[0][1]:.2f}MB) too high"
        assert memory_usage[3][1] < 500.0, f"Memory for 2000 observations ({memory_usage[3][1]:.2f}MB) too high"
        
        # Scaling should be relatively linear (within 2x factor)
        assert 3 < small_ratio < 7, f"Memory scaling ratio {small_ratio:.2f} not linear"
        assert 1.5 < large_ratio < 3, f"Memory scaling ratio {large_ratio:.2f} not linear"
    
    def test_search_performance_scaling(self):
        """Test search performance scaling with data volume."""
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Prepare large dataset
        dataset_sizes = [100, 500, 1000, 2000]
        search_times = []
        
        for size in dataset_sizes:
            AGENT_OBSERVATIONS.clear()
            
            # Store test data
            for i in range(size):
                store_agent_observation(
                    agent_type=f"search-perf-agent-{i % 20}",
                    task_id=f"search_perf_task_{i}",
                    project_id=f"search_project_{i % 100}",
                    category=["performance", "quality", "success", "improvement"][i % 4],
                    content=f"Search performance scaling test observation {i} optimization database query caching performance monitoring metrics analysis",
                    observation_data={"search_test_index": i, "relevance_score": 0.5 + (i % 50) * 0.01},
                    analysis={"search_performance_test": True, "dataset_size": size}
                )
            
            # Test search performance
            timer = PerformanceTimer()
            timer.start()
            
            results = search_agent_observations("optimization performance monitoring", limit=20)
            
            elapsed = timer.stop()
            search_times.append((size, elapsed))
            
            # Verify results quality
            assert len(results["results"]) > 0, f"No results found for dataset size {size}"
            assert len(results["results"]) <= 20, f"Too many results returned for dataset size {size}"
            
            print(f"Search performance for {size} observations: {elapsed:.4f}s")
        
        # Analyze search scaling - should be sub-linear
        for size, elapsed in search_times:
            # All searches should complete within reasonable time
            max_time = 0.1 + (size / 1000) * 0.5  # Allow scaling but keep reasonable
            assert elapsed < max_time, f"Search in {size} observations took {elapsed:.4f}s, max allowed {max_time:.4f}s"
        
        # Search time should not grow exponentially
        ratio_500_100 = search_times[1][1] / search_times[0][1] if search_times[0][1] > 0 else 1
        ratio_2000_1000 = search_times[3][1] / search_times[2][1] if search_times[2][1] > 0 else 1
        
        assert ratio_500_100 < 10, f"Search time scaling ratio {ratio_500_100:.2f} too high"
        assert ratio_2000_1000 < 5, f"Search time scaling ratio {ratio_2000_1000:.2f} too high"
    
    def test_cpu_usage_during_operations(self):
        """Test CPU usage characteristics during intensive operations."""
        import threading
        import time
        
        cpu_usage_samples = []
        monitoring = True
        
        def monitor_cpu():
            """Monitor CPU usage during operations."""
            while monitoring:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                cpu_usage_samples.append(cpu_percent)
        
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.clear()
        
        # Start CPU monitoring
        monitor_thread = threading.Thread(target=monitor_cpu)
        monitor_thread.start()
        
        start_time = time.time()
        
        # Perform intensive operations
        for batch in range(10):
            # Store batch of observations
            for i in range(50):
                store_agent_observation(
                    agent_type=f"cpu-test-agent-{i % 5}",
                    task_id=f"cpu_test_task_{batch}_{i}",
                    project_id=f"cpu_test_project_{batch}",
                    category="performance",
                    content=f"CPU usage test observation {batch}-{i} with comprehensive analysis data",
                    observation_data={"batch": batch, "index": i, "cpu_test": True},
                    analysis={"cpu_intensive": True, "computation_heavy": True}
                )
            
            # Perform searches
            for search_idx in range(5):
                search_agent_observations(f"cpu test batch {batch} observation", limit=10)
        
        end_time = time.time()
        monitoring = False
        monitor_thread.join()
        
        # Analyze CPU usage
        if cpu_usage_samples:
            avg_cpu = sum(cpu_usage_samples) / len(cpu_usage_samples)
            max_cpu = max(cpu_usage_samples)
            operation_time = end_time - start_time
            
            # CPU usage should be reasonable
            assert avg_cpu < 80.0, f"Average CPU usage {avg_cpu:.1f}% too high during operations"
            assert max_cpu < 95.0, f"Maximum CPU usage {max_cpu:.1f}% too high"
            assert operation_time < 30.0, f"Operations took {operation_time:.2f}s, too long"
            
            print(f"CPU usage during intensive operations: Avg={avg_cpu:.1f}%, Max={max_cpu:.1f}%, Time={operation_time:.2f}s")


class TestPerformanceRegression:
    """Test for performance regressions and establish benchmarks."""
    
    def test_baseline_performance_benchmarks(self):
        """Establish baseline performance benchmarks for all operations."""
        benchmarks = {}
        
        # Clear data
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        AGENT_OBSERVATIONS.clear()
        AGENT_METRICS.clear()
        COORDINATION_PATTERNS.clear()
        
        # Benchmark: Store agent observation
        timer = PerformanceTimer()
        timer.start()
        
        store_agent_observation(
            agent_type="benchmark-agent",
            task_id="benchmark_task",
            project_id="benchmark_project", 
            category="performance",
            content="Baseline performance benchmark observation with standard data size and complexity",
            observation_data={"benchmark": True, "data_size": "standard"},
            analysis={"performance_test": True, "baseline_measurement": True}
        )
        
        benchmarks["store_observation"] = timer.stop()
        
        # Benchmark: Search observations (with 100 observations)
        for i in range(99):  # Add 99 more (we already have 1)
            store_agent_observation(
                agent_type=f"benchmark-agent-{i % 10}",
                task_id=f"benchmark_task_{i}",
                project_id=f"benchmark_project_{i % 10}",
                category="performance",
                content=f"Benchmark search data {i} for performance testing",
                observation_data={"index": i},
                analysis={"search_benchmark": True}
            )
        
        timer.start()
        search_agent_observations("benchmark performance testing", limit=20)
        benchmarks["search_observations"] = timer.stop()
        
        # Benchmark: Store agent metric
        measurements = [{"timestamp": f"2024-01-01T{i:02d}:00:00", "value": i * 0.1} for i in range(24)]
        
        timer.start()
        store_agent_metric(
            agent_type="benchmark-agent",
            metric_type="response_time",
            project_id="benchmark_project",
            measurements=measurements
        )
        benchmarks["store_metric"] = timer.stop()
        
        # Benchmark: Coordination pattern analysis
        timer.start()
        analyze_coordination_patterns(
            agent_sequence=["agent-1", "agent-2", "agent-3"],
            pattern_name="Benchmark Pattern",
            project_context="benchmark_project",
            success_metrics={"completion_rate": 0.9}
        )
        benchmarks["analyze_pattern"] = timer.stop()
        
        # Benchmark: Generate insights
        timer.start()
        generate_agent_insights()
        benchmarks["generate_insights"] = timer.stop()
        
        # Performance expectations (these should be updated based on hardware)
        expected_benchmarks = {
            "store_observation": 0.05,   # 50ms
            "search_observations": 0.3,  # 300ms for 100 observations
            "store_metric": 0.1,         # 100ms for 24 measurements  
            "analyze_pattern": 0.05,     # 50ms
            "generate_insights": 0.5     # 500ms for comprehensive analysis
        }
        
        print("Performance Benchmarks:")
        for operation, time_taken in benchmarks.items():
            expected = expected_benchmarks[operation]
            status = "✓" if time_taken <= expected else "⚠"
            print(f"  {operation}: {time_taken:.4f}s (expected ≤ {expected:.3f}s) {status}")
            
            # Warn if significantly over expected time (but don't fail - hardware varies)
            if time_taken > expected * 2:
                print(f"    WARNING: {operation} took {time_taken:.4f}s, significantly over expected {expected:.3f}s")
        
        # Only fail on egregious performance issues
        assert benchmarks["store_observation"] < 0.5, "Store observation critically slow"
        assert benchmarks["search_observations"] < 2.0, "Search critically slow"
        assert benchmarks["store_metric"] < 1.0, "Store metric critically slow"
        assert benchmarks["analyze_pattern"] < 0.5, "Pattern analysis critically slow"
        assert benchmarks["generate_insights"] < 3.0, "Insight generation critically slow"
        
        return benchmarks


if __name__ == "__main__":
    # Run performance tests with verbose output
    pytest.main([__file__, "-v", "-s"])