#!/usr/bin/env python3
"""
Comprehensive test suite for agent observation models.

This module tests all 9 new Pydantic models for:
- Type safety and validation
- Data serialization/deserialization
- Model validation rules and constraints
- Backward compatibility with existing models
"""

import pytest
import json
from datetime import datetime
from typing import Dict, Any, List
from pydantic import ValidationError

# Import all models
from mcp_vector_server.models import (
    # Agent Observation Models
    ObservationMetadata,
    AgentObservationChunk,
    PerformanceMetricMetadata,
    PerformanceMetricChunk,
    CoordinationPatternMetadata,
    CoordinationPatternChunk,
    
    # Query Models
    AgentObservationQuery,
    AgentMetricQuery,
    PatternAnalysisQuery,
    
    # Result Models
    AgentObservationResult,
    AgentMetricResult,
    PatternAnalysisResult,
    
    # Existing Models (for compatibility testing)
    ChunkMetadata,
    DocumentChunk,
    SearchResult,
    SearchQuery
)


class TestObservationMetadata:
    """Test ObservationMetadata model validation and functionality."""
    
    def test_valid_observation_metadata(self):
        """Test creation with valid data."""
        metadata = ObservationMetadata(
            agent_type="backend-agent",
            task_id="task_123",
            project_id="project_abc",
            category="performance",
            complexity="medium",
            feature="user-auth",
            environment="production",
            dependencies=["frontend-agent"],
            timestamp="2024-01-01T12:00:00"
        )
        
        assert metadata.type == "observation"
        assert metadata.agent_type == "backend-agent"
        assert metadata.task_id == "task_123"
        assert metadata.project_id == "project_abc"
        assert metadata.category == "performance"
        assert metadata.complexity == "medium"
        assert metadata.feature == "user-auth"
        assert metadata.environment == "production"
        assert metadata.dependencies == ["frontend-agent"]
        assert metadata.timestamp == "2024-01-01T12:00:00"
    
    def test_automatic_timestamp_generation(self):
        """Test automatic timestamp generation when not provided."""
        metadata = ObservationMetadata(
            agent_type="backend-agent",
            task_id="task_123",
            project_id="project_abc",
            category="performance",
            complexity="medium"
        )
        
        # Should have generated a timestamp
        assert metadata.timestamp is not None
        # Should be a valid ISO format timestamp
        datetime.fromisoformat(metadata.timestamp)
    
    def test_invalid_category(self):
        """Test validation of category field."""
        with pytest.raises(ValidationError) as exc_info:
            ObservationMetadata(
                agent_type="backend-agent",
                task_id="task_123",
                project_id="project_abc",
                category="invalid_category",  # Invalid category
                complexity="medium"
            )
        
        assert "category" in str(exc_info.value)
    
    def test_invalid_complexity(self):
        """Test validation of complexity field."""
        with pytest.raises(ValidationError) as exc_info:
            ObservationMetadata(
                agent_type="backend-agent",
                task_id="task_123",
                project_id="project_abc",
                category="performance",
                complexity="invalid_complexity"  # Invalid complexity
            )
        
        assert "complexity" in str(exc_info.value)
    
    def test_required_fields(self):
        """Test that required fields raise ValidationError when missing."""
        with pytest.raises(ValidationError) as exc_info:
            ObservationMetadata(
                agent_type="backend-agent",
                task_id="task_123",
                # Missing project_id and category
                complexity="medium"
            )
        
        error_str = str(exc_info.value)
        assert "project_id" in error_str
        assert "category" in error_str


class TestAgentObservationChunk:
    """Test AgentObservationChunk model validation and functionality."""
    
    def test_valid_observation_chunk(self):
        """Test creation with valid data."""
        metadata = ObservationMetadata(
            agent_type="backend-agent",
            task_id="task_123",
            project_id="project_abc",
            category="performance",
            complexity="medium"
        )
        
        chunk = AgentObservationChunk(
            chunk_id="obs_12345678",
            content="Backend agent completed API endpoint implementation with 95% test coverage",
            metadata=metadata,
            observation_data={
                "execution_time": 1.2,
                "memory_usage": 45.6,
                "test_coverage": 0.95
            },
            analysis={
                "performance_score": 0.87,
                "quality_indicators": ["high_coverage", "fast_execution"],
                "improvement_areas": ["memory_optimization"]
            },
            recommendations=["Optimize memory usage in user query processing"],
            correlations=["obs_87654321"],
            parent_doc="project_abc_backend",
            position=1,
            tokens=15
        )
        
        assert chunk.chunk_id == "obs_12345678"
        assert "API endpoint implementation" in chunk.content
        assert chunk.metadata.agent_type == "backend-agent"
        assert chunk.observation_data["execution_time"] == 1.2
        assert chunk.analysis["performance_score"] == 0.87
        assert len(chunk.recommendations) == 1
        assert len(chunk.correlations) == 1
        assert chunk.tokens == 15
    
    def test_serialization_deserialization(self):
        """Test JSON serialization and deserialization."""
        metadata = ObservationMetadata(
            agent_type="frontend-agent",
            task_id="task_456",
            project_id="project_xyz",
            category="quality",
            complexity="high"
        )
        
        original_chunk = AgentObservationChunk(
            chunk_id="obs_87654321",
            content="Frontend agent implemented responsive design with accessibility compliance",
            metadata=metadata,
            observation_data={"render_time": 0.8, "accessibility_score": 0.96},
            analysis={"user_experience": "excellent", "performance": "good"},
            recommendations=["Add keyboard navigation shortcuts"],
            correlations=["obs_11111111"]
        )
        
        # Serialize to JSON
        json_data = original_chunk.model_dump_json()
        parsed_data = json.loads(json_data)
        
        # Deserialize back to model
        restored_chunk = AgentObservationChunk.model_validate(parsed_data)
        
        assert restored_chunk.chunk_id == original_chunk.chunk_id
        assert restored_chunk.content == original_chunk.content
        assert restored_chunk.metadata.agent_type == original_chunk.metadata.agent_type
        assert restored_chunk.observation_data == original_chunk.observation_data
        assert restored_chunk.analysis == original_chunk.analysis


class TestPerformanceMetricModels:
    """Test PerformanceMetricMetadata and PerformanceMetricChunk models."""
    
    def test_valid_performance_metric_metadata(self):
        """Test creation with valid performance metric metadata."""
        metadata = PerformanceMetricMetadata(
            agent_type="testing-agent",
            metric_type="response_time",
            aggregation_period="hour",
            project_id="project_123",
            timestamp="2024-01-01T12:00:00"
        )
        
        assert metadata.type == "metric"
        assert metadata.agent_type == "testing-agent"
        assert metadata.metric_type == "response_time"
        assert metadata.aggregation_period == "hour"
        assert metadata.project_id == "project_123"
    
    def test_performance_metric_chunk(self):
        """Test creation with valid performance metric chunk."""
        metadata = PerformanceMetricMetadata(
            agent_type="backend-agent",
            metric_type="task_completion_rate",
            aggregation_period="day",
            project_id="project_abc"
        )
        
        measurements = [
            {"timestamp": "2024-01-01T09:00:00", "value": 0.95, "task_count": 20},
            {"timestamp": "2024-01-01T10:00:00", "value": 0.87, "task_count": 15},
            {"timestamp": "2024-01-01T11:00:00", "value": 0.92, "task_count": 18}
        ]
        
        statistics = {
            "mean": 0.913,
            "median": 0.92,
            "std_dev": 0.034,
            "min": 0.87,
            "max": 0.95
        }
        
        thresholds = {
            "excellent": 0.95,
            "good": 0.85,
            "acceptable": 0.70,
            "poor": 0.50
        }
        
        chunk = PerformanceMetricChunk(
            chunk_id="metric_12345",
            content="Backend agent task completion rate over 3 hours",
            metadata=metadata,
            measurements=measurements,
            statistics=statistics,
            thresholds=thresholds,
            trends={"direction": "stable", "slope": 0.02}
        )
        
        assert len(chunk.measurements) == 3
        assert chunk.statistics["mean"] == 0.913
        assert chunk.thresholds["excellent"] == 0.95
        assert chunk.trends["direction"] == "stable"


class TestCoordinationPatternModels:
    """Test CoordinationPatternMetadata and CoordinationPatternChunk models."""
    
    def test_valid_coordination_pattern_metadata(self):
        """Test creation with valid coordination pattern metadata."""
        metadata = CoordinationPatternMetadata(
            pattern_name="Sequential Backend-Frontend",
            agent_sequence=["planning-agent", "backend-agent", "frontend-agent", "testing-agent"],
            complexity_suitability=["medium", "high"],
            project_context="e-commerce-app",
            timestamp="2024-01-01T15:30:00"
        )
        
        assert metadata.type == "pattern"
        assert metadata.pattern_name == "Sequential Backend-Frontend"
        assert len(metadata.agent_sequence) == 4
        assert "backend-agent" in metadata.agent_sequence
        assert metadata.complexity_suitability == ["medium", "high"]
    
    def test_coordination_pattern_chunk(self):
        """Test creation with valid coordination pattern chunk."""
        metadata = CoordinationPatternMetadata(
            pattern_name="Parallel Research Implementation",
            agent_sequence=["control-agent", "research-agent", "backend-agent"],
            complexity_suitability=["high", "critical"],
            project_context="ai-platform"
        )
        
        success_metrics = {
            "completion_rate": 0.94,
            "time_efficiency": 0.87,
            "quality_score": 0.91,
            "coordination_overhead": 0.15
        }
        
        applicable_scenarios = [
            "New feature development with unknown APIs",
            "Complex integration requiring research",
            "Multi-technology stack implementation"
        ]
        
        chunk = CoordinationPatternChunk(
            chunk_id="pattern_abc123",
            content="Parallel research and implementation pattern with 94% success rate",
            metadata=metadata,
            success_metrics=success_metrics,
            applicable_scenarios=applicable_scenarios,
            resource_requirements={"agents": 3, "time_hours": 4.5, "coordination_calls": 8},
            historical_performance=[
                {"date": "2024-01-01", "success": True, "duration": 4.2},
                {"date": "2024-01-02", "success": True, "duration": 4.8},
                {"date": "2024-01-03", "success": False, "duration": 6.1}
            ],
            optimizations=[
                {"type": "communication", "description": "Reduce check-in frequency to 45 minutes"}
            ]
        )
        
        assert chunk.success_metrics["completion_rate"] == 0.94
        assert len(chunk.applicable_scenarios) == 3
        assert chunk.resource_requirements["agents"] == 3
        assert len(chunk.historical_performance) == 3
        assert len(chunk.optimizations) == 1


class TestQueryModels:
    """Test all query models for agent observations."""
    
    def test_agent_observation_query(self):
        """Test AgentObservationQuery validation."""
        query = AgentObservationQuery(
            query="performance optimization recommendations",
            limit=20,
            agent_type="backend-agent",
            category="improvement",
            project_id="project_123",
            task_id="task_456",
            complexity="high",
            min_similarity=0.75,
            time_range={"start": "2024-01-01T00:00:00", "end": "2024-01-31T23:59:59"}
        )
        
        assert query.query == "performance optimization recommendations"
        assert query.limit == 20
        assert query.agent_type == "backend-agent"
        assert query.category == "improvement"
        assert query.min_similarity == 0.75
        assert query.time_range["start"] == "2024-01-01T00:00:00"
    
    def test_agent_observation_query_validation(self):
        """Test query validation limits."""
        # Test limit validation
        with pytest.raises(ValidationError):
            AgentObservationQuery(
                query="test",
                limit=101  # Above maximum limit of 100
            )
        
        with pytest.raises(ValidationError):
            AgentObservationQuery(
                query="test",
                limit=0  # Below minimum limit of 1
            )
        
        # Test similarity validation
        with pytest.raises(ValidationError):
            AgentObservationQuery(
                query="test",
                min_similarity=1.5  # Above maximum of 1.0
            )
    
    def test_agent_metric_query(self):
        """Test AgentMetricQuery validation."""
        query = AgentMetricQuery(
            agent_type="frontend-agent",
            metric_type="response_time",
            time_range={"start": "2024-01-01T00:00:00", "end": "2024-01-01T23:59:59"},
            aggregation="hourly",
            project_id="project_xyz"
        )
        
        assert query.agent_type == "frontend-agent"
        assert query.metric_type == "response_time"
        assert query.aggregation == "hourly"
        assert query.project_id == "project_xyz"
    
    def test_pattern_analysis_query(self):
        """Test PatternAnalysisQuery validation."""
        query = PatternAnalysisQuery(
            pattern_name="Sequential Development",
            agent_sequence=["planning-agent", "backend-agent", "testing-agent"],
            complexity_level="medium",
            project_id="project_123",
            min_success_rate=0.8
        )
        
        assert query.pattern_name == "Sequential Development"
        assert len(query.agent_sequence) == 3
        assert query.complexity_level == "medium"
        assert query.min_success_rate == 0.8


class TestResultModels:
    """Test all result models for agent observations."""
    
    def test_agent_observation_result(self):
        """Test AgentObservationResult model."""
        # Create a sample observation chunk
        metadata = ObservationMetadata(
            agent_type="testing-agent",
            task_id="task_789",
            project_id="project_test",
            category="quality",
            complexity="low"
        )
        
        chunk = AgentObservationChunk(
            chunk_id="obs_test123",
            content="Testing agent completed unit test suite with 98% coverage",
            metadata=metadata,
            observation_data={"test_count": 45, "pass_rate": 0.98, "execution_time": 2.3},
            analysis={"quality_score": 0.96, "areas_covered": ["unit", "integration"]}
        )
        
        result = AgentObservationResult(
            chunk=chunk,
            similarity=0.87,
            rank=1
        )
        
        assert result.chunk.chunk_id == "obs_test123"
        assert result.similarity == 0.87
        assert result.rank == 1
        assert result.chunk.observation_data["test_count"] == 45
    
    def test_agent_metric_result(self):
        """Test AgentMetricResult model."""
        metadata = PerformanceMetricMetadata(
            agent_type="control-agent",
            metric_type="coordination_efficiency",
            aggregation_period="day",
            project_id="project_coordination"
        )
        
        chunk = PerformanceMetricChunk(
            chunk_id="metric_coord123",
            content="Control agent coordination efficiency metrics",
            metadata=metadata,
            measurements=[{"value": 0.91, "timestamp": "2024-01-01T12:00:00"}],
            statistics={"mean": 0.91},
            thresholds={"good": 0.85},
            trends={"direction": "improving"}
        )
        
        result = AgentMetricResult(
            chunk=chunk,
            aggregated_value=0.91,
            trend="improving",
            rank=2
        )
        
        assert result.chunk.chunk_id == "metric_coord123"
        assert result.aggregated_value == 0.91
        assert result.trend == "improving"
        assert result.rank == 2


class TestBackwardCompatibility:
    """Test backward compatibility with existing models."""
    
    def test_existing_chunk_metadata_compatibility(self):
        """Test that existing ChunkMetadata still works."""
        metadata = ChunkMetadata(
            type="text",
            source_url="https://example.com/docs",
            doc_title="API Reference",
            category="api_reference",
            complexity=0.7
        )
        
        assert metadata.type == "text"
        assert metadata.category == "api_reference"
        assert metadata.complexity == 0.7
    
    def test_existing_document_chunk_compatibility(self):
        """Test that existing DocumentChunk still works."""
        metadata = ChunkMetadata(
            type="code",
            category="examples"
        )
        
        chunk = DocumentChunk(
            chunk_id="doc_123",
            content="function example() { return 'hello'; }",
            metadata=metadata,
            parent_doc="javascript_guide",
            position=5,
            tokens=8
        )
        
        assert chunk.chunk_id == "doc_123"
        assert chunk.metadata.type == "code"
        assert chunk.tokens == 8
    
    def test_existing_search_functionality(self):
        """Test that existing search models still work."""
        # Create a traditional document chunk
        doc_metadata = ChunkMetadata(type="text", category="guides")
        doc_chunk = DocumentChunk(
            chunk_id="guide_123",
            content="How to use React hooks",
            metadata=doc_metadata
        )
        
        # Create search result
        search_result = SearchResult(
            chunk=doc_chunk,
            similarity=0.92,
            rank=1
        )
        
        assert search_result.chunk.chunk_id == "guide_123"
        assert search_result.similarity == 0.92
        
        # Create search query
        query = SearchQuery(
            query="React hooks tutorial",
            limit=10,
            category="guides",
            min_similarity=0.3
        )
        
        assert query.query == "React hooks tutorial"
        assert query.category == "guides"
        assert query.limit == 10


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_string_validation(self):
        """Test handling of empty strings in required fields."""
        with pytest.raises(ValidationError):
            ObservationMetadata(
                agent_type="",  # Empty string
                task_id="task_123",
                project_id="project_abc",
                category="performance",
                complexity="medium"
            )
    
    def test_none_values_in_optional_fields(self):
        """Test that None values are acceptable in optional fields."""
        metadata = ObservationMetadata(
            agent_type="backend-agent",
            task_id="task_123",
            project_id="project_abc",
            category="performance",
            complexity="medium",
            feature=None,  # Optional field
            environment="development"
        )
        
        assert metadata.feature is None
        assert metadata.environment == "development"
    
    def test_large_data_structures(self):
        """Test handling of large data structures."""
        # Create large observation data
        large_observation_data = {
            f"metric_{i}": i * 0.1 for i in range(1000)
        }
        
        metadata = ObservationMetadata(
            agent_type="backend-agent",
            task_id="large_task",
            project_id="large_project",
            category="performance",
            complexity="high"
        )
        
        chunk = AgentObservationChunk(
            chunk_id="obs_large",
            content="Large dataset processing observation",
            metadata=metadata,
            observation_data=large_observation_data,
            analysis={"processed_items": 1000, "performance": "good"}
        )
        
        assert len(chunk.observation_data) == 1000
        assert chunk.analysis["processed_items"] == 1000
    
    def test_unicode_content_handling(self):
        """Test handling of Unicode content."""
        metadata = ObservationMetadata(
            agent_type="documentation-agent",
            task_id="unicode_task",
            project_id="i18n_project",
            category="quality",
            complexity="medium"
        )
        
        unicode_content = "Documentation updated with émojis 🚀 and spëcial characters ñ"
        
        chunk = AgentObservationChunk(
            chunk_id="obs_unicode",
            content=unicode_content,
            metadata=metadata,
            observation_data={"chars_processed": len(unicode_content)},
            analysis={"encoding": "utf-8", "special_chars": 6}
        )
        
        assert chunk.content == unicode_content
        assert "🚀" in chunk.content
        assert "ñ" in chunk.content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])