"""Data models for the vector database."""

from typing import Dict, Any, Optional, List, Union, Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator


class ChunkMetadata(BaseModel):
    """Metadata for a documentation chunk."""
    type: str  # text, code, etc.
    source_url: Optional[str] = None
    scraped_at: Optional[str] = None
    doc_title: Optional[str] = None
    category: Optional[str] = None  # getting_started, guides, api_reference, etc.
    complexity: Optional[float] = None
    parent_title: Optional[str] = None
    source_file: Optional[str] = None
    section_level: Optional[int] = None
    section_title: Optional[str] = None


class DocumentChunk(BaseModel):
    """A single chunk of documentation with metadata."""
    chunk_id: str
    content: str
    metadata: ChunkMetadata
    parent_doc: Optional[str] = None
    position: Optional[int] = None
    tokens: Optional[int] = None


class SearchResult(BaseModel):
    """Result from semantic search."""
    chunk: DocumentChunk
    similarity: float
    rank: int


class SearchQuery(BaseModel):
    """Search query parameters."""
    query: str
    limit: int = 10
    category: Optional[str] = None
    technology: Optional[str] = None
    doc_type: Optional[str] = None  # text, code, etc.
    min_similarity: float = 0.3


class TechnologyMapping(BaseModel):
    """Mapping for technology keywords to documentation."""
    name: str
    keywords: List[str]
    categories: List[str]
    file_patterns: List[str]


# Technology mappings for the documentation
TECH_MAPPINGS = [
    TechnologyMapping(
        name="Convex",
        keywords=["convex", "database", "backend", "realtime"],
        categories=["getting_started", "guides", "api_reference"],
        file_patterns=["*Convex*", "*convex*"]
    ),
    TechnologyMapping(
        name="Shadcn/ui",
        keywords=["shadcn", "ui", "components", "design system"],
        categories=["getting_started", "guides", "examples"],
        file_patterns=["*Shadcn*", "*shadcn*"]
    ),
    TechnologyMapping(
        name="RadixUI",
        keywords=["radix", "primitives", "themes", "colors", "ui"],
        categories=["getting_started", "guides", "examples"],
        file_patterns=["*RadixUi*", "*Radix*"]
    ),
    TechnologyMapping(
        name="TailwindCSS",
        keywords=["tailwind", "css", "styling", "utility"],
        categories=["getting_started", "guides", "examples"],
        file_patterns=["*tailwindCSS*", "*tailwind*"]
    ),
    TechnologyMapping(
        name="Kiro",
        keywords=["kiro", "mcp", "agent", "ai"],
        categories=["getting_started", "guides", "mcp"],
        file_patterns=["*Kiro*", "*kiro*"]
    ),
    TechnologyMapping(
        name="Claude Code",
        keywords=["claude", "code", "anthropic", "ai", "mcp"],
        categories=["getting_started", "guides", "setup"],
        file_patterns=["*Claude*", "*Anthropic*", "*claude*"]
    ),
    TechnologyMapping(
        name="Clerk",
        keywords=["clerk", "auth", "authentication", "user"],
        categories=["getting_started", "guides", "authentication"],
        file_patterns=["*Clerk*", "*clerk*"]
    ),
    TechnologyMapping(
        name="Polar",
        keywords=["polar", "billing", "subscriptions", "payments"],
        categories=["getting_started", "guides", "api_reference"],
        file_patterns=["*Polar*", "*polar*"]
    ),
    TechnologyMapping(
        name="React",
        keywords=["react", "jsx", "components", "hooks"],
        categories=["getting_started", "guides", "examples"],
        file_patterns=["*React*", "*react*"]
    ),
]


# Category descriptions
CATEGORY_DESCRIPTIONS = {
    "getting_started": "Quick start guides and installation instructions",
    "concepts": "Core concepts and architectural explanations", 
    "guides": "Step-by-step tutorials and how-to guides",
    "api_reference": "API documentation and reference materials",
    "examples": "Code examples and sample implementations",
    "advanced": "Advanced topics and detailed configurations",
    "troubleshooting": "Common issues and solutions",
    "mcp": "Model Context Protocol related documentation",
    "setup": "Installation and setup instructions",
    "authentication": "Authentication and security documentation",
    "agent_observations": "Agent behavior observations and performance data",
    "agent_metrics": "Agent performance metrics and analytics",
    "coordination_patterns": "Multi-agent coordination patterns and workflows"
}


# Agent Observation Models - Extension for Agent System Integration

class ObservationMetadata(BaseModel):
    """Metadata for agent observation chunks."""
    type: Literal["observation"] = "observation"
    agent_type: str = Field(..., description="Type of agent making the observation")
    task_id: str = Field(..., description="Unique identifier for the task")
    project_id: str = Field(..., description="Project identifier for cross-project analysis")
    category: Literal["performance", "quality", "coordination", "error", "success", "improvement"] = Field(..., description="Observation category")
    complexity: Literal["low", "medium", "high", "critical"] = Field(..., description="Task complexity level")
    feature: Optional[str] = Field(None, description="Feature or component being worked on")
    environment: str = Field(default="development", description="Environment where observation occurred")
    dependencies: List[str] = Field(default_factory=list, description="Other agents or tasks this depends on")
    timestamp: str = Field(..., description="ISO timestamp when observation was made")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.now().isoformat()


class AgentObservationChunk(BaseModel):
    """Agent observation data chunk for vector database storage."""
    chunk_id: str = Field(..., description="Unique identifier for this observation")
    content: str = Field(..., description="Human-readable observation content for semantic search")
    metadata: ObservationMetadata = Field(..., description="Observation metadata")
    
    # Structured observation data
    observation_data: Dict[str, Any] = Field(..., description="Structured observation metrics and data")
    analysis: Dict[str, Any] = Field(..., description="Analysis results and insights")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")
    correlations: List[str] = Field(default_factory=list, description="Related observations or patterns")
    
    # Vector database compatibility
    parent_doc: Optional[str] = Field(None, description="Parent document for grouping")
    position: Optional[int] = Field(None, description="Position in sequence")
    tokens: Optional[int] = Field(None, description="Token count for content")


class PerformanceMetricMetadata(BaseModel):
    """Metadata for agent performance metrics."""
    type: Literal["metric"] = "metric"
    agent_type: str = Field(..., description="Agent type being measured")
    metric_type: Literal["response_time", "task_completion_rate", "quality_score", "coordination_efficiency", "commit_frequency"] = Field(..., description="Type of metric")
    aggregation_period: Literal["minute", "hour", "day", "week"] = Field(..., description="Time period for aggregation")
    project_id: str = Field(..., description="Project context for metric")
    timestamp: str = Field(..., description="Measurement timestamp")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.now().isoformat()


class PerformanceMetricChunk(BaseModel):
    """Performance metric data chunk for agent analytics."""
    chunk_id: str = Field(..., description="Unique identifier for this metric")
    content: str = Field(..., description="Human-readable metric description")
    metadata: PerformanceMetricMetadata = Field(..., description="Metric metadata")
    
    # Metric data
    measurements: List[Dict[str, Any]] = Field(..., description="Time series measurement data")
    statistics: Dict[str, float] = Field(..., description="Statistical analysis (mean, median, std_dev)")
    thresholds: Dict[str, float] = Field(..., description="Performance thresholds (excellent, good, acceptable, poor)")
    trends: Dict[str, Any] = Field(..., description="Trend analysis data")
    
    # Vector database compatibility
    parent_doc: Optional[str] = Field(None, description="Parent document for grouping")
    position: Optional[int] = Field(None, description="Position in sequence")
    tokens: Optional[int] = Field(None, description="Token count for content")


class CoordinationPatternMetadata(BaseModel):
    """Metadata for coordination patterns."""
    type: Literal["pattern"] = "pattern"
    pattern_name: str = Field(..., description="Name of the coordination pattern")
    agent_sequence: List[str] = Field(..., description="Sequence of agents in the pattern")
    complexity_suitability: List[str] = Field(..., description="Task complexity levels this pattern suits")
    project_context: str = Field(..., description="Project where pattern was observed")
    timestamp: str = Field(..., description="Pattern observation timestamp")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.now().isoformat()


class CoordinationPatternChunk(BaseModel):
    """Coordination pattern data chunk for workflow optimization."""
    chunk_id: str = Field(..., description="Unique identifier for this pattern")
    content: str = Field(..., description="Human-readable pattern description")
    metadata: CoordinationPatternMetadata = Field(..., description="Pattern metadata")
    
    # Pattern data
    success_metrics: Dict[str, float] = Field(..., description="Pattern effectiveness metrics")
    applicable_scenarios: List[str] = Field(..., description="Scenarios where pattern applies")
    resource_requirements: Dict[str, float] = Field(..., description="Resource usage requirements")
    historical_performance: List[Dict[str, Any]] = Field(..., description="Historical execution data")
    optimizations: List[Dict[str, Any]] = Field(..., description="Potential optimizations")
    
    # Vector database compatibility
    parent_doc: Optional[str] = Field(None, description="Parent document for grouping")
    position: Optional[int] = Field(None, description="Position in sequence")
    tokens: Optional[int] = Field(None, description="Token count for content")


# Search query extensions for agent observations
class AgentObservationQuery(BaseModel):
    """Search query for agent observations."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results to return")
    agent_type: Optional[str] = Field(None, description="Filter by agent type")
    category: Optional[str] = Field(None, description="Filter by observation category") 
    project_id: Optional[str] = Field(None, description="Filter by project")
    task_id: Optional[str] = Field(None, description="Filter by task")
    complexity: Optional[str] = Field(None, description="Filter by complexity level")
    min_similarity: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity score")
    time_range: Optional[Dict[str, str]] = Field(None, description="Time range filter (start, end)")


class AgentMetricQuery(BaseModel):
    """Search query for agent performance metrics."""
    agent_type: str = Field(..., description="Agent type to query")
    metric_type: Optional[str] = Field(None, description="Specific metric type")
    time_range: Dict[str, str] = Field(..., description="Time range for metrics (start, end)")
    aggregation: Literal["raw", "hourly", "daily", "weekly"] = Field(default="daily", description="Aggregation level")
    project_id: Optional[str] = Field(None, description="Filter by project")


class PatternAnalysisQuery(BaseModel):
    """Query for coordination pattern analysis."""
    pattern_name: Optional[str] = Field(None, description="Specific pattern name")
    agent_sequence: Optional[List[str]] = Field(None, description="Required agent sequence")
    complexity_level: Optional[str] = Field(None, description="Task complexity filter")
    project_id: Optional[str] = Field(None, description="Project context")
    min_success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum success rate")


# Result models for agent queries
class AgentObservationResult(BaseModel):
    """Result from agent observation search."""
    chunk: AgentObservationChunk
    similarity: float
    rank: int


class AgentMetricResult(BaseModel):
    """Result from agent metric query."""
    chunk: PerformanceMetricChunk
    aggregated_value: float
    trend: str
    rank: int


class PatternAnalysisResult(BaseModel):
    """Result from pattern analysis."""
    chunk: CoordinationPatternChunk
    effectiveness_score: float
    recommendation_strength: float
    rank: int