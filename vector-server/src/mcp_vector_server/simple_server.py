#!/usr/bin/env python3
"""Simple MCP Vector Server implementation."""

import asyncio
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import our extended models for agent observations
try:
    from .models import (
        AgentObservationChunk, PerformanceMetricChunk, CoordinationPatternChunk,
        AgentObservationQuery, AgentMetricQuery, PatternAnalysisQuery,
        AgentObservationResult, AgentMetricResult, PatternAnalysisResult
    )
except ImportError:
    # Fallback if models can't be imported
    logger.warning("Could not import agent observation models - agent features disabled")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple database loader
def load_vector_database():
    """Load vector database from path."""
    db_path = os.getenv("VECTOR_DB_PATH")
    if not db_path:
        logger.info("No VECTOR_DB_PATH set, using demo data")
        return [
            {"chunk_id": "demo_1", "content": "React hooks documentation", "category": "guides"},
            {"chunk_id": "demo_2", "content": "Claude Code setup guide", "category": "setup"}
        ]
    
    index_file = Path(db_path) / "vector_db_index.json"
    if not index_file.exists():
        logger.error(f"Database index not found: {index_file}")
        return []
    
    with open(index_file, 'r') as f:
        chunks = json.load(f)
    
    logger.info(f"Loaded {len(chunks)} chunks from {db_path}")
    return chunks

# Global database
DATABASE = None
AGENT_OBSERVATIONS = []  # In-memory storage for agent observations
AGENT_METRICS = []  # In-memory storage for agent metrics  
COORDINATION_PATTERNS = []  # In-memory storage for coordination patterns

def get_database():
    """Get loaded database."""
    global DATABASE
    if DATABASE is None:
        DATABASE = load_vector_database()
    return DATABASE

def search_documentation(query: str, limit: int = 10, **filters):
    """Search documentation."""
    chunks = get_database()
    
    # Split query into terms for better matching
    query_terms = query.lower().split()
    results = []
    
    for chunk in chunks:
        content = chunk.get('content', '').lower()
        
        # Score based on term matches
        score = 0
        for term in query_terms:
            if term in content:
                score += content.count(term)
        
        if score > 0:  # Found at least one term
            results.append({
                "chunk": {
                    "chunk_id": chunk.get('chunk_id', 'unknown'),
                    "content": chunk.get('content', ''),
                    "metadata": chunk.get('metadata', {}),
                    "tokens": len(chunk.get('content', '').split())
                },
                "similarity": min(0.95, 0.3 + (score * 0.1)),  # Score-based similarity
                "rank": 0,  # Will be set after sorting
                "score": score
            })
    
    # Sort by score and assign ranks
    results.sort(key=lambda x: x['score'], reverse=True)
    for i, result in enumerate(results[:limit]):
        result['rank'] = i + 1
        del result['score']  # Remove internal score
    
    return {"results": results[:limit]}


# Agent Observation Functions - New MCP Tool Implementations

def store_agent_observation(agent_type: str, task_id: str, project_id: str, category: str, 
                           content: str, observation_data: Dict[str, Any], 
                           analysis: Dict[str, Any], **kwargs) -> str:
    """Store an agent observation in the vector database."""
    try:
        # Generate unique observation ID
        observation_id = f"obs_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        # Create observation structure compatible with existing database
        observation = {
            "chunk_id": observation_id,
            "content": content,
            "metadata": {
                "type": "observation",
                "agent_type": agent_type,
                "task_id": task_id,
                "project_id": project_id,
                "category": category,
                "timestamp": timestamp,
                "complexity": kwargs.get("complexity", "medium"),
                "feature": kwargs.get("feature"),
                "environment": kwargs.get("environment", "development"),
                "dependencies": kwargs.get("dependencies", [])
            },
            "observation_data": observation_data,
            "analysis": analysis,
            "recommendations": kwargs.get("recommendations", []),
            "correlations": kwargs.get("correlations", []),
            "tokens": len(content.split())
        }
        
        # Store in global observations list
        global AGENT_OBSERVATIONS
        AGENT_OBSERVATIONS.append(observation)
        
        logger.info(f"Stored agent observation: {observation_id} for {agent_type}")
        return observation_id
        
    except Exception as e:
        logger.error(f"Error storing agent observation: {e}")
        raise


def search_agent_observations(query: str, limit: int = 10, **filters) -> Dict[str, Any]:
    """Search agent observations with semantic matching."""
    try:
        global AGENT_OBSERVATIONS
        query_terms = query.lower().split()
        results = []
        
        for obs in AGENT_OBSERVATIONS:
            content = obs.get('content', '').lower()
            metadata = obs.get('metadata', {})
            
            # Apply filters
            if filters.get('agent_type') and metadata.get('agent_type') != filters['agent_type']:
                continue
            if filters.get('category') and metadata.get('category') != filters['category']:
                continue
            if filters.get('project_id') and metadata.get('project_id') != filters['project_id']:
                continue
            if filters.get('task_id') and metadata.get('task_id') != filters['task_id']:
                continue
                
            # Score based on term matches
            score = 0
            for term in query_terms:
                if term in content:
                    score += content.count(term)
                # Also search in analysis data
                analysis_str = str(obs.get('analysis', {})).lower()
                if term in analysis_str:
                    score += analysis_str.count(term) * 0.5
            
            if score > 0:
                results.append({
                    "chunk": obs,
                    "similarity": min(0.95, 0.3 + (score * 0.15)),
                    "rank": 0,
                    "score": score
                })
        
        # Sort by score and assign ranks
        results.sort(key=lambda x: x['score'], reverse=True)
        for i, result in enumerate(results[:limit]):
            result['rank'] = i + 1
            del result['score']
            
        return {"results": results[:limit]}
        
    except Exception as e:
        logger.error(f"Error searching agent observations: {e}")
        return {"results": [], "error": str(e)}


def store_agent_metric(agent_type: str, metric_type: str, project_id: str, 
                      measurements: List[Dict[str, Any]], **kwargs) -> str:
    """Store agent performance metrics."""
    try:
        metric_id = f"metric_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        # Calculate basic statistics
        values = [m.get('value', 0) for m in measurements if isinstance(m.get('value'), (int, float))]
        statistics = {}
        if values:
            statistics = {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "count": len(values)
            }
        
        metric = {
            "chunk_id": metric_id,
            "content": f"{agent_type} {metric_type} performance metric",
            "metadata": {
                "type": "metric",
                "agent_type": agent_type,
                "metric_type": metric_type,
                "project_id": project_id,
                "timestamp": timestamp,
                "aggregation_period": kwargs.get("aggregation_period", "hour")
            },
            "measurements": measurements,
            "statistics": statistics,
            "thresholds": kwargs.get("thresholds", {}),
            "trends": kwargs.get("trends", {}),
            "tokens": len(f"{agent_type} {metric_type}".split())
        }
        
        global AGENT_METRICS
        AGENT_METRICS.append(metric)
        
        logger.info(f"Stored agent metric: {metric_id} for {agent_type}")
        return metric_id
        
    except Exception as e:
        logger.error(f"Error storing agent metric: {e}")
        raise


def analyze_coordination_patterns(agent_sequence: List[str], pattern_name: str, 
                                 project_context: str, **kwargs) -> Dict[str, Any]:
    """Analyze and store coordination patterns."""
    try:
        pattern_id = f"pattern_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        # Basic pattern analysis
        success_metrics = kwargs.get("success_metrics", {})
        historical_data = kwargs.get("historical_performance", [])
        
        pattern = {
            "chunk_id": pattern_id,
            "content": f"Coordination pattern: {pattern_name} with sequence {' -> '.join(agent_sequence)}",
            "metadata": {
                "type": "pattern",
                "pattern_name": pattern_name,
                "agent_sequence": agent_sequence,
                "project_context": project_context,
                "timestamp": timestamp,
                "complexity_suitability": kwargs.get("complexity_suitability", ["medium"])
            },
            "success_metrics": success_metrics,
            "applicable_scenarios": kwargs.get("applicable_scenarios", []),
            "resource_requirements": kwargs.get("resource_requirements", {}),
            "historical_performance": historical_data,
            "optimizations": kwargs.get("optimizations", []),
            "tokens": len(pattern_name.split()) + len(agent_sequence)
        }
        
        global COORDINATION_PATTERNS
        COORDINATION_PATTERNS.append(pattern)
        
        # Return analysis results
        return {
            "pattern_id": pattern_id,
            "effectiveness_score": success_metrics.get("completion_rate", 0.0),
            "optimization_suggestions": pattern.get("optimizations", []),
            "applicable_scenarios": pattern.get("applicable_scenarios", [])
        }
        
    except Exception as e:
        logger.error(f"Error analyzing coordination pattern: {e}")
        return {"error": str(e)}


def generate_agent_insights(agent_type: Optional[str] = None, time_range: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Generate insights from agent observations and metrics."""
    try:
        global AGENT_OBSERVATIONS, AGENT_METRICS, COORDINATION_PATTERNS
        
        insights = {
            "summary": {},
            "performance_trends": {},
            "recommendations": [],
            "patterns": []
        }
        
        # Filter data by agent type if specified
        observations = AGENT_OBSERVATIONS
        metrics = AGENT_METRICS
        patterns = COORDINATION_PATTERNS
        
        if agent_type:
            observations = [obs for obs in observations 
                          if obs.get('metadata', {}).get('agent_type') == agent_type]
            metrics = [metric for metric in metrics 
                      if metric.get('metadata', {}).get('agent_type') == agent_type]
        
        # Generate basic insights
        insights["summary"] = {
            "total_observations": len(observations),
            "total_metrics": len(metrics),
            "total_patterns": len(patterns),
            "agent_types": list(set(obs.get('metadata', {}).get('agent_type', 'unknown') 
                                   for obs in observations))
        }
        
        # Extract recommendations from observations
        all_recommendations = []
        for obs in observations:
            all_recommendations.extend(obs.get('recommendations', []))
        
        insights["recommendations"] = list(set(all_recommendations))[:10]  # Top 10 unique recommendations
        
        # Pattern effectiveness
        pattern_effectiveness = []
        for pattern in patterns:
            effectiveness = pattern.get('success_metrics', {}).get('completion_rate', 0.0)
            pattern_effectiveness.append({
                "pattern_name": pattern.get('metadata', {}).get('pattern_name', 'unknown'),
                "effectiveness": effectiveness,
                "agent_sequence": pattern.get('metadata', {}).get('agent_sequence', [])
            })
        
        insights["patterns"] = sorted(pattern_effectiveness, key=lambda x: x['effectiveness'], reverse=True)[:5]
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generating agent insights: {e}")
        return {"error": str(e)}

def handle_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request."""
    try:
        method = request_data.get("method")
        params = request_data.get("params", {})
        request_id = request_data.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "vector-search",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "initialized":
            # This is a notification, no response needed
            return None
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "search_documentation",
                            "description": "Search technical documentation",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search query"},
                                    "limit": {"type": "integer", "default": 10}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "store_agent_observation",
                            "description": "Store agent behavior observation for improvement analysis",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "agent_type": {"type": "string", "description": "Type of agent making observation"},
                                    "task_id": {"type": "string", "description": "Unique task identifier"},
                                    "project_id": {"type": "string", "description": "Project identifier"},
                                    "category": {"type": "string", "enum": ["performance", "quality", "coordination", "error", "success", "improvement"]},
                                    "content": {"type": "string", "description": "Human-readable observation description"},
                                    "observation_data": {"type": "object", "description": "Structured observation metrics"},
                                    "analysis": {"type": "object", "description": "Analysis results and insights"},
                                    "recommendations": {"type": "array", "items": {"type": "string"}, "description": "Improvement recommendations"},
                                    "complexity": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "medium"},
                                    "feature": {"type": "string", "description": "Feature or component being worked on"},
                                    "environment": {"type": "string", "default": "development"}
                                },
                                "required": ["agent_type", "task_id", "project_id", "category", "content", "observation_data", "analysis"]
                            }
                        },
                        {
                            "name": "search_agent_observations",
                            "description": "Search agent observations with filters",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search query"},
                                    "limit": {"type": "integer", "default": 10},
                                    "agent_type": {"type": "string", "description": "Filter by agent type"},
                                    "category": {"type": "string", "description": "Filter by observation category"},
                                    "project_id": {"type": "string", "description": "Filter by project"},
                                    "task_id": {"type": "string", "description": "Filter by task"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "store_agent_metric",
                            "description": "Store agent performance metrics",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "agent_type": {"type": "string", "description": "Agent type being measured"},
                                    "metric_type": {"type": "string", "enum": ["response_time", "task_completion_rate", "quality_score", "coordination_efficiency", "commit_frequency"]},
                                    "project_id": {"type": "string", "description": "Project context"},
                                    "measurements": {"type": "array", "items": {"type": "object"}, "description": "Time series measurements"},
                                    "thresholds": {"type": "object", "description": "Performance thresholds"},
                                    "aggregation_period": {"type": "string", "enum": ["minute", "hour", "day", "week"], "default": "hour"}
                                },
                                "required": ["agent_type", "metric_type", "project_id", "measurements"]
                            }
                        },
                        {
                            "name": "analyze_coordination_patterns",
                            "description": "Analyze and store agent coordination patterns",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "agent_sequence": {"type": "array", "items": {"type": "string"}, "description": "Sequence of agents in pattern"},
                                    "pattern_name": {"type": "string", "description": "Name of coordination pattern"},
                                    "project_context": {"type": "string", "description": "Project where pattern was observed"},
                                    "success_metrics": {"type": "object", "description": "Pattern effectiveness metrics"},
                                    "applicable_scenarios": {"type": "array", "items": {"type": "string"}, "description": "Applicable scenarios"},
                                    "complexity_suitability": {"type": "array", "items": {"type": "string"}, "description": "Suitable complexity levels"}
                                },
                                "required": ["agent_sequence", "pattern_name", "project_context"]
                            }
                        },
                        {
                            "name": "generate_agent_insights",
                            "description": "Generate insights from agent observations and metrics",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "agent_type": {"type": "string", "description": "Filter by specific agent type"},
                                    "time_range": {"type": "object", "description": "Time range for analysis"}
                                },
                                "required": []
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "search_documentation":
                result = search_documentation(**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            
            elif tool_name == "store_agent_observation":
                observation_id = store_agent_observation(**arguments)
                result = {"observation_id": observation_id, "status": "stored"}
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            
            elif tool_name == "search_agent_observations":
                result = search_agent_observations(**arguments)
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            
            elif tool_name == "store_agent_metric":
                metric_id = store_agent_metric(**arguments)
                result = {"metric_id": metric_id, "status": "stored"}
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            
            elif tool_name == "analyze_coordination_patterns":
                result = analyze_coordination_patterns(**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            
            elif tool_name == "generate_agent_insights":
                result = generate_agent_insights(**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        }
        
    except Exception as e:
        logger.error(f"Request handling error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_data.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

async def main():
    """Main server loop."""
    logger.info("Simple MCP Vector Server starting...")
    
    # Load database
    database = get_database()
    logger.info(f"Database ready with {len(database)} chunks")
    
    logger.info("Server ready for connections")
    
    try:
        # Read from stdin
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON-RPC request
                try:
                    request = json.loads(line)
                    response = handle_request(request)
                    if response is not None:
                        print(json.dumps(response))
                        sys.stdout.flush()
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"}
                    }
                    print(json.dumps(error_response))
                    sys.stdout.flush()
                    
            except EOFError:
                break
            except KeyboardInterrupt:
                break
                
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        logger.info("Server shutting down")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server interrupted")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)