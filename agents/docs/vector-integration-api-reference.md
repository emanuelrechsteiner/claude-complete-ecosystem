# Vector Database Agent Observation API Reference

**Version**: 1.0.0  
**Protocol**: MCP (Model Context Protocol) JSON-RPC 2.0  
**Status**: Production Ready ✅

This document provides comprehensive API reference for the 5 new MCP tools that enable agent observation tracking and improvement analysis through the integrated vector database system.

## Overview

The Vector Database Agent Observation system extends the existing production vector database with specialized tools for agent behavior tracking, performance analytics, and workflow optimization. All tools maintain sub-second response times and provide comprehensive error handling.

## Authentication & Setup

### Prerequisites
- MCP-compatible client (Claude Code, Cursor, VS Code)
- Vector database server running at configured endpoint
- Proper environment variables configured

### Environment Configuration
```bash
# Required environment variables
export VECTOR_DB_PATH="/path/to/vector/database"
export LOG_LEVEL="INFO"
export MCP_SERVER_PORT="8080"
```

### MCP Client Configuration
```json
{
  "mcpServers": {
    "vector-agent-observations": {
      "command": "python",
      "args": ["/path/to/mcp-vector-server/src/mcp_vector_server/simple_server.py"],
      "env": {
        "VECTOR_DB_PATH": "/path/to/vector/database",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## API Tools Reference

### 1. store_agent_observation

**Purpose**: Store agent behavior observations for improvement analysis

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "agent_type": {
      "type": "string",
      "description": "Type of agent making observation",
      "enum": ["planning", "research", "backend", "frontend", "testing", "documentation", "version-control", "control"]
    },
    "task_id": {
      "type": "string",
      "description": "Unique task identifier",
      "pattern": "^[a-zA-Z0-9_-]+$"
    },
    "project_id": {
      "type": "string", 
      "description": "Project identifier for cross-project analysis"
    },
    "category": {
      "type": "string",
      "enum": ["performance", "quality", "coordination", "error", "success", "improvement"],
      "description": "Observation category for classification"
    },
    "content": {
      "type": "string",
      "description": "Human-readable observation description",
      "minLength": 10,
      "maxLength": 2000
    },
    "observation_data": {
      "type": "object",
      "description": "Structured observation metrics and data",
      "additionalProperties": true
    },
    "analysis": {
      "type": "object", 
      "description": "Analysis results and insights",
      "properties": {
        "trend": {"type": "string", "enum": ["improving", "declining", "stable", "anomaly"]},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "impact": {"type": "string", "enum": ["high", "medium", "low"]}
      }
    },
    "recommendations": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Improvement recommendations"
    },
    "complexity": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "default": "medium"
    },
    "feature": {
      "type": "string",
      "description": "Feature or component being worked on"
    },
    "environment": {
      "type": "string",
      "default": "development",
      "enum": ["development", "staging", "production"]
    }
  },
  "required": ["agent_type", "task_id", "project_id", "category", "content", "observation_data", "analysis"]
}
```

**Usage Example**:
```javascript
await mcp_client.call_tool("store_agent_observation", {
  "agent_type": "backend",
  "task_id": "api_implementation_user_auth",
  "project_id": "task_management_system",
  "category": "performance",
  "content": "Successfully implemented user authentication API with JWT tokens, achieving 95ms average response time",
  "observation_data": {
    "response_time_ms": 95,
    "endpoints_implemented": 5,
    "test_coverage": 0.92,
    "security_score": 0.95
  },
  "analysis": {
    "trend": "improving",
    "confidence": 0.95,
    "impact": "high"
  },
  "recommendations": [
    "Consider implementing response caching for 10ms improvement",
    "Add rate limiting for production deployment",
    "Enhance error logging for better debugging"
  ],
  "complexity": "high",
  "feature": "user_authentication",
  "environment": "development"
});
```

**Response**:
```json
{
  "observation_id": "obs_a1b2c3d4", 
  "status": "stored",
  "timestamp": "2024-01-21T10:30:00Z"
}
```

**Performance**: ~1ms typical response time

---

### 2. search_agent_observations

**Purpose**: Search agent observations with semantic matching and advanced filtering

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Semantic search query",
      "minLength": 1
    },
    "limit": {
      "type": "integer",
      "default": 10,
      "minimum": 1,
      "maximum": 100
    },
    "agent_type": {
      "type": "string",
      "description": "Filter by agent type"
    },
    "category": {
      "type": "string", 
      "description": "Filter by observation category"
    },
    "project_id": {
      "type": "string",
      "description": "Filter by project"
    },
    "task_id": {
      "type": "string",
      "description": "Filter by specific task"
    },
    "complexity": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Filter by complexity level"
    },
    "min_similarity": {
      "type": "number",
      "default": 0.3,
      "minimum": 0.0,
      "maximum": 1.0
    },
    "time_range": {
      "type": "object",
      "properties": {
        "start": {"type": "string", "format": "date-time"},
        "end": {"type": "string", "format": "date-time"}
      }
    }
  },
  "required": ["query"]
}
```

**Usage Example**:
```javascript
await mcp_client.call_tool("search_agent_observations", {
  "query": "coordination efficiency backend frontend handoff patterns",
  "limit": 15,
  "category": "coordination",
  "project_id": "task_management_system",
  "min_similarity": 0.4,
  "time_range": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-31T23:59:59Z"
  }
});
```

**Response**:
```json
{
  "results": [
    {
      "chunk": {
        "chunk_id": "obs_a1b2c3d4",
        "content": "Observed efficient coordination pattern between backend and frontend agents...",
        "metadata": {
          "agent_type": "control",
          "task_id": "coordination_optimization", 
          "project_id": "task_management_system",
          "category": "coordination",
          "timestamp": "2024-01-15T14:30:00Z"
        },
        "observation_data": {...},
        "analysis": {...},
        "recommendations": [...]
      },
      "similarity": 0.87,
      "rank": 1
    }
  ],
  "total_found": 15,
  "query_time_ms": 45
}
```

**Performance**: ~50ms typical response time

---

### 3. store_agent_metric

**Purpose**: Store agent performance metrics with automatic statistical analysis

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "agent_type": {
      "type": "string",
      "description": "Agent type being measured"
    },
    "metric_type": {
      "type": "string",
      "enum": ["response_time", "task_completion_rate", "quality_score", "coordination_efficiency", "commit_frequency"],
      "description": "Type of performance metric"
    },
    "project_id": {
      "type": "string",
      "description": "Project context for metric"
    },
    "measurements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": {"type": "string", "format": "date-time"},
          "value": {"type": "number"},
          "context": {"type": "object"}
        },
        "required": ["timestamp", "value"]
      },
      "minItems": 1
    },
    "thresholds": {
      "type": "object",
      "properties": {
        "excellent": {"type": "number"},
        "good": {"type": "number"},
        "acceptable": {"type": "number"}, 
        "poor": {"type": "number"}
      }
    },
    "aggregation_period": {
      "type": "string",
      "enum": ["minute", "hour", "day", "week"],
      "default": "hour"
    }
  },
  "required": ["agent_type", "metric_type", "project_id", "measurements"]
}
```

**Usage Example**:
```javascript
await mcp_client.call_tool("store_agent_metric", {
  "agent_type": "backend",
  "metric_type": "response_time", 
  "project_id": "task_management_system",
  "measurements": [
    {
      "timestamp": "2024-01-21T10:00:00Z",
      "value": 95,
      "context": {"operation": "user_auth", "complexity": "high"}
    },
    {
      "timestamp": "2024-01-21T10:05:00Z", 
      "value": 87,
      "context": {"operation": "user_auth", "complexity": "high"}
    }
  ],
  "thresholds": {
    "excellent": 50,
    "good": 100, 
    "acceptable": 200,
    "poor": 500
  },
  "aggregation_period": "hour"
});
```

**Response**:
```json
{
  "metric_id": "metric_x1y2z3a4",
  "status": "stored",
  "statistics": {
    "mean": 91.0,
    "min": 87, 
    "max": 95,
    "count": 2
  },
  "performance_rating": "good"
}
```

**Performance**: ~10ms typical response time

---

### 4. analyze_coordination_patterns

**Purpose**: Analyze and store multi-agent coordination patterns for workflow optimization

**Input Schema**:
```json
{
  "type": "object", 
  "properties": {
    "agent_sequence": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 2,
      "description": "Sequence of agents in coordination pattern"
    },
    "pattern_name": {
      "type": "string",
      "description": "Descriptive name for coordination pattern"
    },
    "project_context": {
      "type": "string", 
      "description": "Project where pattern was observed"
    },
    "success_metrics": {
      "type": "object",
      "properties": {
        "completion_rate": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "average_duration": {"type": "number", "minimum": 0},
        "quality_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "conflict_rate": {"type": "number", "minimum": 0.0, "maximum": 1.0}
      }
    },
    "applicable_scenarios": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Scenarios where pattern is effective"
    },
    "complexity_suitability": {
      "type": "array",
      "items": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
      "description": "Task complexity levels this pattern suits"
    },
    "resource_requirements": {
      "type": "object",
      "description": "Resource consumption metrics"
    },
    "historical_performance": {
      "type": "array",
      "items": {"type": "object"}
    }
  },
  "required": ["agent_sequence", "pattern_name", "project_context"]
}
```

**Usage Example**:
```javascript
await mcp_client.call_tool("analyze_coordination_patterns", {
  "agent_sequence": ["planning", "research", "backend", "frontend", "testing", "documentation"],
  "pattern_name": "full_stack_feature_development",
  "project_context": "task_management_system",
  "success_metrics": {
    "completion_rate": 0.95,
    "average_duration": 6.5,
    "quality_score": 0.88,
    "conflict_rate": 0.05
  },
  "applicable_scenarios": [
    "new_feature_development",
    "api_endpoint_creation", 
    "database_schema_changes"
  ],
  "complexity_suitability": ["medium", "high", "critical"],
  "resource_requirements": {
    "total_agent_hours": 18,
    "peak_concurrent_agents": 3,
    "communication_overhead": 0.15
  }
});
```

**Response**:
```json
{
  "pattern_id": "pattern_f5g6h7i8",
  "effectiveness_score": 0.91,
  "optimization_suggestions": [
    "Consider parallel execution of research and planning phases",
    "Add automated testing checkpoints between frontend and testing",
    "Implement documentation templates to reduce documentation time"
  ],
  "applicable_scenarios": [
    "new_feature_development",
    "api_endpoint_creation", 
    "database_schema_changes"
  ],
  "estimated_improvement": 0.15
}
```

**Performance**: ~5ms typical response time

---

### 5. generate_agent_insights

**Purpose**: Generate comprehensive insights from all stored observations and metrics

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "agent_type": {
      "type": "string",
      "description": "Filter insights by specific agent type (optional)"
    },
    "project_id": {
      "type": "string", 
      "description": "Filter insights by project (optional)"
    },
    "time_range": {
      "type": "object",
      "properties": {
        "start": {"type": "string", "format": "date-time"},
        "end": {"type": "string", "format": "date-time"}
      },
      "description": "Time range for analysis (optional)"
    },
    "focus_areas": {
      "type": "array",
      "items": {"type": "string", "enum": ["performance", "coordination", "quality", "efficiency"]},
      "description": "Specific areas to focus analysis on"
    },
    "include_predictions": {
      "type": "boolean",
      "default": true,
      "description": "Include predictive insights"
    }
  }
}
```

**Usage Example**:
```javascript
await mcp_client.call_tool("generate_agent_insights", {
  "agent_type": "backend",
  "project_id": "task_management_system",
  "time_range": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-31T23:59:59Z"
  },
  "focus_areas": ["performance", "quality"],
  "include_predictions": true
});
```

**Response**:
```json
{
  "summary": {
    "total_observations": 156,
    "total_metrics": 89,
    "total_patterns": 12,
    "agent_types_analyzed": ["backend", "frontend", "testing"],
    "time_range_days": 31
  },
  "performance_trends": {
    "response_time": {
      "trend": "improving",
      "change_percent": -15.3,
      "current_average": 98.5,
      "prediction_next_month": 85.2
    },
    "quality_score": {
      "trend": "stable", 
      "change_percent": 2.1,
      "current_average": 0.89,
      "prediction_next_month": 0.91
    }
  },
  "recommendations": [
    "Implement response caching to achieve sub-90ms response times",
    "Add automated quality gates to maintain 0.90+ quality scores",
    "Consider load balancing for peak traffic optimization"
  ],
  "patterns": [
    {
      "pattern_name": "api_development_workflow",
      "effectiveness": 0.94,
      "agent_sequence": ["planning", "backend", "testing"],
      "usage_frequency": 23
    }
  ],
  "predictions": {
    "expected_performance_improvement": 0.18,
    "recommended_optimizations": 3,
    "confidence_level": 0.87
  },
  "insights_generated_at": "2024-01-21T15:45:00Z"
}
```

**Performance**: ~200ms typical response time

## Error Handling

### Standard Error Response Format
```json
{
  "jsonrpc": "2.0",
  "id": "request_id",
  "error": {
    "code": -32603,
    "message": "Internal error: Detailed error description",
    "data": {
      "error_type": "ValidationError",
      "field": "agent_type",
      "details": "Additional context"
    }
  }
}
```

### Common Error Codes
- `-32700`: Parse error (Invalid JSON)
- `-32600`: Invalid Request (Malformed JSON-RPC)
- `-32601`: Method not found (Unknown tool name)
- `-32602`: Invalid params (Schema validation failed)
- `-32603`: Internal error (Server-side processing error)

### Error Recovery Strategies
1. **Validation Errors**: Check input parameters against schema
2. **Timeout Errors**: Retry with exponential backoff
3. **Storage Errors**: Verify database connectivity and permissions
4. **Memory Errors**: Reduce batch sizes and implement pagination

## Performance Optimization

### Batch Operations
For high-volume scenarios, consider batching multiple observations:

```javascript
// Instead of multiple individual calls
for (let obs of observations) {
  await store_agent_observation(obs);
}

// Use batch processing approach
await Promise.all(observations.map(obs => store_agent_observation(obs)));
```

### Caching Strategies
- **Search Results**: Cache frequently accessed observation queries
- **Insights Generation**: Cache daily insight reports for reuse
- **Pattern Analysis**: Cache pattern effectiveness scores

### Memory Management
- **Observation Cleanup**: Regular cleanup of old observations
- **Metric Aggregation**: Aggregate historical metrics to reduce storage
- **Pattern Archival**: Archive unused coordination patterns

## Security Considerations

### Data Privacy
- All observations are project-scoped and isolated
- No cross-project data leakage in search results
- Sensitive data should be excluded from observation content

### Access Control
- Implement authentication for MCP client connections
- Use environment variables for sensitive configuration
- Regular security audits of observation data

### Data Retention
- Configure automatic cleanup of old observations
- Implement data archival strategies for compliance
- Ensure GDPR compliance for user-related observations

## Monitoring & Diagnostics

### Performance Monitoring
- Track response times for all tool calls
- Monitor memory usage and resource consumption
- Set up alerts for performance degradation

### Health Checks
```bash
# Basic server health check
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### Logging Configuration
```python
# Recommended logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vector_db_agent.log'),
        logging.StreamHandler()
    ]
)
```

---

**API Version**: 1.0.0  
**Last Updated**: January 21, 2024  
**Contact**: Integration Team  
**Support**: See troubleshooting guide for common issues