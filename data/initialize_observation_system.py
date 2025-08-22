#!/usr/bin/env python3
"""
Initialize the agent observation system for cross-project learning.
This enables AI agents to record observations and improve over time.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import uuid

def create_observation_structure():
    """Create the initial observation system structure."""
    return {
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "observations": [],
        "patterns": {},
        "improvements": [],
        "metrics": {
            "total_observations": 0,
            "total_patterns": 0,
            "total_improvements": 0,
            "projects_tracked": 0
        }
    }

def create_sample_observation():
    """Create a sample observation to demonstrate the system."""
    return {
        "id": f"obs_{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now().isoformat(),
        "agent": "control-agent",
        "project": "claude-complete-ecosystem",
        "type": "system_initialization",
        "description": "Agent observation system initialized successfully",
        "metadata": {
            "action": "initialize",
            "component": "observation_system",
            "status": "success",
            "performance": {
                "execution_time": 0.001,
                "memory_usage": "minimal"
            }
        },
        "insights": [
            "Observation system ready for cross-project tracking",
            "AI agents can now record and learn from development patterns"
        ],
        "recommendations": []
    }

def initialize_ledgers(ledger_dir: Path):
    """Initialize agent ledger files."""
    ledgers = [
        "control-tasks.json",
        "backend-tasks.json",
        "frontend-tasks.json",
        "planning-tasks.json",
        "research-tasks.json",
        "testing-tasks.json",
        "documentation-tasks.json",
        "version-control-tasks.json",
        "ui-tasks.json",
        "ux-tasks.json",
        "improvement-tasks.json"
    ]
    
    ledger_template = {
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "tasks": [],
        "completed_count": 0,
        "in_progress_count": 0,
        "pending_count": 0
    }
    
    for ledger_name in ledgers:
        ledger_file = ledger_dir / ledger_name
        if not ledger_file.exists():
            with open(ledger_file, 'w') as f:
                json.dump(ledger_template, f, indent=2)
            print(f"   ✅ Initialized {ledger_name}")

def initialize_global_observation(global_obs_dir: Path):
    """Initialize global observation ledger."""
    observation_ledger = {
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "global_observations": [],
        "cross_project_patterns": {},
        "improvement_suggestions": [],
        "metrics": {
            "total_projects": 0,
            "total_observations": 0,
            "total_patterns": 0,
            "total_improvements": 0,
            "most_active_agent": None,
            "common_issues": [],
            "success_patterns": []
        }
    }
    
    ledger_file = global_obs_dir / "observation-ledger.json"
    if not ledger_file.exists():
        with open(ledger_file, 'w') as f:
            json.dump(observation_ledger, f, indent=2)
        print("   ✅ Initialized global observation ledger")

def main():
    """Main initialization function."""
    # Paths
    script_dir = Path(__file__).parent
    vector_db_dir = script_dir / "vector_db"
    indices_dir = vector_db_dir / "indices"
    
    # Also prepare paths for agent system (in user home)
    home_claude_dir = Path.home() / ".claude"
    ledgers_dir = home_claude_dir / "ledgers"
    global_obs_dir = home_claude_dir / "global-observation"
    
    print("🔍 Initializing Agent Observation System")
    print("=" * 50)
    
    # Ensure directories exist
    indices_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize agent observations in vector database
    print("📊 Setting up vector database observation storage...")
    obs_file = indices_dir / "agent_observations.json"
    
    if obs_file.exists():
        with open(obs_file, 'r') as f:
            observations = json.load(f)
        print(f"   ℹ️ Existing observations found: {len(observations)} entries")
    else:
        observations = []
    
    # Add sample observation if empty
    if not observations:
        sample_obs = create_sample_observation()
        observations.append(sample_obs)
        print("   ✅ Added sample observation")
    
    # Save observations
    with open(obs_file, 'w') as f:
        json.dump(observations, f, indent=2)
    print(f"   ✅ Agent observations initialized ({len(observations)} entries)")
    
    # Initialize observation metadata
    obs_metadata_file = indices_dir / "observation_metadata.json"
    obs_metadata = {
        "version": "1.0.0",
        "initialized_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "total_observations": len(observations),
        "observation_types": ["system_initialization", "task_completion", "error_recovery", "performance_optimization"],
        "tracked_agents": [
            "control-agent", "backend-agent", "frontend-agent", "planning-agent",
            "research-agent", "testing-agent", "documentation-agent", "version-control-agent"
        ],
        "features": {
            "cross_project_tracking": True,
            "pattern_recognition": True,
            "improvement_suggestions": True,
            "performance_metrics": True
        }
    }
    
    with open(obs_metadata_file, 'w') as f:
        json.dump(obs_metadata, f, indent=2)
    print("   ✅ Observation metadata initialized")
    
    # Initialize ledgers if they don't exist
    if ledgers_dir.exists():
        print("\n📝 Checking agent ledgers...")
        initialize_ledgers(ledgers_dir)
    else:
        print("   ℹ️ Agent ledgers will be created during agent system installation")
    
    # Initialize global observation if directory exists
    if global_obs_dir.exists():
        print("\n🌍 Checking global observation system...")
        initialize_global_observation(global_obs_dir)
    else:
        print("   ℹ️ Global observation will be created during agent system installation")
    
    # Create observation system configuration
    obs_config_file = vector_db_dir / "config" / "observation_config.json"
    obs_config = {
        "version": "1.0.0",
        "enabled": True,
        "storage_backend": "vector_database",
        "retention_days": 90,
        "auto_analyze": True,
        "pattern_detection": {
            "enabled": True,
            "min_occurrences": 3,
            "confidence_threshold": 0.75
        },
        "improvement_generation": {
            "enabled": True,
            "frequency": "weekly",
            "min_observations": 10
        },
        "metrics_tracking": {
            "enabled": True,
            "track_performance": True,
            "track_errors": True,
            "track_patterns": True
        }
    }
    
    (vector_db_dir / "config").mkdir(exist_ok=True)
    with open(obs_config_file, 'w') as f:
        json.dump(obs_config, f, indent=2)
    print("\n⚙️ Observation system configuration created")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ Agent Observation System Initialized!")
    print(f"📊 Summary:")
    print(f"   • Observation storage: Ready")
    print(f"   • Cross-project tracking: Enabled")
    print(f"   • Pattern recognition: Enabled")
    print(f"   • Improvement suggestions: Enabled")
    print(f"   • Location: {obs_file}")
    print(f"\n💡 The system will now:")
    print(f"   • Record agent activities across projects")
    print(f"   • Identify successful patterns")
    print(f"   • Generate improvement suggestions")
    print(f"   • Track performance metrics")
    
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)