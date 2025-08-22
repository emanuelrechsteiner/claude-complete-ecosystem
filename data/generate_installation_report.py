#!/usr/bin/env python3
"""
Generate comprehensive installation report for Claude Complete Ecosystem.
This script validates all components and creates a detailed status report.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

def check_file_exists(file_path: Path) -> bool:
    """Check if a file exists and is not empty."""
    return file_path.exists() and file_path.stat().st_size > 0

def check_directory_exists(dir_path: Path) -> bool:
    """Check if a directory exists and has content."""
    return dir_path.exists() and any(dir_path.iterdir())

def test_vector_database(vector_db_dir: Path) -> Dict[str, Any]:
    """Test vector database status and content."""
    results = {
        "status": "unknown",
        "total_chunks": 0,
        "categories": [],
        "has_index": False,
        "has_observations": False,
        "errors": []
    }
    
    try:
        # Check vector index
        index_file = vector_db_dir / "vector_db_index.json"
        if check_file_exists(index_file):
            with open(index_file, 'r') as f:
                index_data = json.load(f)
                results["total_chunks"] = len(index_data)
                results["has_index"] = True
                categories = set()
                for entry in index_data:
                    if "metadata" in entry and "category" in entry["metadata"]:
                        categories.add(entry["metadata"]["category"])
                results["categories"] = sorted(list(categories))
        
        # Check observations
        obs_file = vector_db_dir / "indices" / "agent_observations.json"
        if check_file_exists(obs_file):
            with open(obs_file, 'r') as f:
                obs_data = json.load(f)
                results["has_observations"] = len(obs_data) > 0
        
        # Determine status
        if results["total_chunks"] > 0:
            results["status"] = "populated"
        elif results["has_index"]:
            results["status"] = "empty"
        else:
            results["status"] = "not_initialized"
    
    except Exception as e:
        results["errors"].append(str(e))
        results["status"] = "error"
    
    return results

def test_agent_system(home_dir: Path) -> Dict[str, Any]:
    """Test agent system installation."""
    results = {
        "installed": False,
        "global_config": False,
        "agents_count": 0,
        "ledgers_ready": False,
        "observation_ready": False,
        "errors": []
    }
    
    claude_dir = home_dir / ".claude"
    
    try:
        # Check global config
        if check_file_exists(claude_dir / "CLAUDE.md"):
            results["global_config"] = True
        
        # Count agents
        agents_dir = claude_dir / "agents"
        if agents_dir.exists():
            agent_files = list(agents_dir.glob("*.md"))
            results["agents_count"] = len(agent_files)
            results["installed"] = len(agent_files) > 0
        
        # Check ledgers
        ledgers_dir = claude_dir / "ledgers"
        if check_directory_exists(ledgers_dir):
            results["ledgers_ready"] = True
        
        # Check observation
        obs_dir = claude_dir / "global-observation"
        if check_file_exists(obs_dir / "observation-ledger.json"):
            results["observation_ready"] = True
    
    except Exception as e:
        results["errors"].append(str(e))
    
    return results

def test_mcp_integration(home_dir: Path) -> Dict[str, Any]:
    """Test MCP server integration."""
    results = {
        "configured": False,
        "vector_search": False,
        "firecrawl": False,
        "config_path": None,
        "errors": []
    }
    
    config_file = home_dir / ".claude" / "claude_desktop_config.json"
    
    try:
        if check_file_exists(config_file):
            results["configured"] = True
            results["config_path"] = str(config_file)
            
            with open(config_file, 'r') as f:
                config = json.load(f)
                
            if "mcpServers" in config:
                if "vector-search" in config["mcpServers"]:
                    results["vector_search"] = True
                if "firecrawl" in config["mcpServers"]:
                    results["firecrawl"] = True
    
    except Exception as e:
        results["errors"].append(str(e))
    
    return results

def test_doc_tools(doc_tools_dir: Path) -> Dict[str, Any]:
    """Test documentation tools installation."""
    results = {
        "installed": False,
        "venv_ready": False,
        "scraper_available": False,
        "processor_available": False,
        "gui_available": False,
        "errors": []
    }
    
    try:
        # Check virtual environment
        if (doc_tools_dir / "venv").exists():
            results["venv_ready"] = True
        
        # Check scripts
        if check_file_exists(doc_tools_dir / "SimpleDocScraper.py"):
            results["scraper_available"] = True
        
        if check_file_exists(doc_tools_dir / "DocPostProcessor.py"):
            results["processor_available"] = True
        
        if check_file_exists(doc_tools_dir / "DocScraperGUI.py"):
            results["gui_available"] = True
        
        results["installed"] = (results["venv_ready"] and 
                              results["scraper_available"] and 
                              results["processor_available"])
    
    except Exception as e:
        results["errors"].append(str(e))
    
    return results

def test_vector_server(vector_server_dir: Path) -> Dict[str, Any]:
    """Test vector server installation."""
    results = {
        "installed": False,
        "venv_ready": False,
        "module_importable": False,
        "errors": []
    }
    
    try:
        # Check virtual environment
        if (vector_server_dir / "venv").exists():
            results["venv_ready"] = True
        
        # Check if module exists
        if check_file_exists(vector_server_dir / "src" / "mcp_vector_server" / "__init__.py"):
            results["module_importable"] = True
        
        results["installed"] = results["venv_ready"] and results["module_importable"]
    
    except Exception as e:
        results["errors"].append(str(e))
    
    return results

def calculate_success_rate(test_results: Dict[str, Any]) -> float:
    """Calculate overall success rate."""
    total_checks = 0
    passed_checks = 0
    
    # Vector database checks
    if test_results["vector_database"]["status"] == "populated":
        passed_checks += 3  # index, chunks, categories
    total_checks += 3
    
    # Agent system checks
    if test_results["agent_system"]["installed"]:
        passed_checks += 1
    if test_results["agent_system"]["global_config"]:
        passed_checks += 1
    if test_results["agent_system"]["observation_ready"]:
        passed_checks += 1
    total_checks += 3
    
    # MCP integration checks
    if test_results["mcp_integration"]["configured"]:
        passed_checks += 1
    if test_results["mcp_integration"]["vector_search"]:
        passed_checks += 1
    total_checks += 2
    
    # Doc tools checks
    if test_results["doc_tools"]["installed"]:
        passed_checks += 1
    total_checks += 1
    
    # Vector server checks
    if test_results["vector_server"]["installed"]:
        passed_checks += 1
    total_checks += 1
    
    return (passed_checks / total_checks * 100) if total_checks > 0 else 0

def generate_markdown_report(test_results: Dict[str, Any], output_file: Path):
    """Generate markdown installation report."""
    success_rate = calculate_success_rate(test_results)
    
    # Determine overall status
    if success_rate >= 90:
        overall_status = "✅ SUCCESS - FULLY FUNCTIONAL"
        status_emoji = "🎉"
    elif success_rate >= 70:
        overall_status = "⚠️ PARTIAL SUCCESS - MOSTLY FUNCTIONAL"
        status_emoji = "⚡"
    else:
        overall_status = "❌ FAILED - NEEDS ATTENTION"
        status_emoji = "🔧"
    
    report = f"""# Claude Complete Ecosystem - Installation Report

## {status_emoji} Installation Status: {overall_status}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Success Rate**: {success_rate:.1f}%

---

## 📊 Component Status

### 1. Vector Database - {test_results['vector_database']['status'].upper()}
- **Total Chunks**: {test_results['vector_database']['total_chunks']}
- **Categories**: {', '.join(test_results['vector_database']['categories']) if test_results['vector_database']['categories'] else 'None'}
- **Has Index**: {'✅ Yes' if test_results['vector_database']['has_index'] else '❌ No'}
- **Observations Ready**: {'✅ Yes' if test_results['vector_database']['has_observations'] else '❌ No'}

### 2. Agent System - {'INSTALLED' if test_results['agent_system']['installed'] else 'NOT INSTALLED'}
- **Global Config**: {'✅ Yes' if test_results['agent_system']['global_config'] else '❌ No'}
- **Agents Count**: {test_results['agent_system']['agents_count']}
- **Ledgers Ready**: {'✅ Yes' if test_results['agent_system']['ledgers_ready'] else '❌ No'}
- **Observation System**: {'✅ Ready' if test_results['agent_system']['observation_ready'] else '❌ Not Ready'}

### 3. MCP Integration - {'CONFIGURED' if test_results['mcp_integration']['configured'] else 'NOT CONFIGURED'}
- **Config File**: {'✅ Found' if test_results['mcp_integration']['configured'] else '❌ Not Found'}
- **Vector Search**: {'✅ Configured' if test_results['mcp_integration']['vector_search'] else '❌ Not Configured'}
- **Firecrawl**: {'✅ Configured' if test_results['mcp_integration']['firecrawl'] else '⚠️ Not Configured (Optional)'}

### 4. Documentation Tools - {'INSTALLED' if test_results['doc_tools']['installed'] else 'NOT INSTALLED'}
- **Virtual Environment**: {'✅ Ready' if test_results['doc_tools']['venv_ready'] else '❌ Not Ready'}
- **Scraper**: {'✅ Available' if test_results['doc_tools']['scraper_available'] else '❌ Missing'}
- **Post-Processor**: {'✅ Available' if test_results['doc_tools']['processor_available'] else '❌ Missing'}
- **GUI Tools**: {'✅ Available' if test_results['doc_tools']['gui_available'] else '❌ Missing'}

### 5. Vector Server - {'INSTALLED' if test_results['vector_server']['installed'] else 'NOT INSTALLED'}
- **Virtual Environment**: {'✅ Ready' if test_results['vector_server']['venv_ready'] else '❌ Not Ready'}
- **Module**: {'✅ Importable' if test_results['vector_server']['module_importable'] else '❌ Not Importable'}

---

## 🔍 Detailed Analysis

"""
    
    # Add success features
    if success_rate >= 70:
        report += """### ✅ Working Features
"""
        if test_results['vector_database']['total_chunks'] > 0:
            report += f"- **Vector Search**: {test_results['vector_database']['total_chunks']} documentation chunks ready for semantic search\n"
        if test_results['agent_system']['installed']:
            report += f"- **Agent Coordination**: {test_results['agent_system']['agents_count']} agents ready for multi-agent workflows\n"
        if test_results['agent_system']['observation_ready']:
            report += "- **Cross-Project Learning**: Observation system ready to track and improve\n"
        if test_results['doc_tools']['installed']:
            report += "- **Documentation Processing**: Tools ready to scrape and process new documentation\n"
        if test_results['mcp_integration']['vector_search']:
            report += "- **MCP Integration**: Vector search integrated with Claude Code\n"
        report += "\n"
    
    # Add issues if any
    all_errors = []
    for component in test_results.values():
        if isinstance(component, dict) and "errors" in component:
            all_errors.extend(component["errors"])
    
    if all_errors or success_rate < 100:
        report += """### ⚠️ Issues Found
"""
        if not test_results['vector_database']['has_index']:
            report += "- Vector database needs to be populated with documentation\n"
        if not test_results['agent_system']['global_config']:
            report += "- Agent system global configuration missing\n"
        if not test_results['mcp_integration']['configured']:
            report += "- MCP integration not configured in Claude Code\n"
        if test_results['vector_database']['total_chunks'] == 0:
            report += "- No documentation chunks indexed yet\n"
        
        for error in all_errors:
            report += f"- Error: {error}\n"
        report += "\n"
    
    # Add next steps
    report += """## 🚀 Next Steps

"""
    
    if success_rate >= 90:
        report += """**Your ecosystem is ready to use!**

1. Restart Claude Code to load the new configuration
2. Test vector search with queries about Claude Code
3. Let agents coordinate automatically on your projects
4. Scrape additional documentation as needed

### Quick Test Commands:
```bash
# Test vector search
cd vector-server && source venv/bin/activate
VECTOR_DB_PATH="../data/vector_db" python -c "from mcp_vector_server.simple_server import search_documentation; print(search_documentation('memory management'))"

# Scrape new documentation
cd doc-tools && source venv/bin/activate
python SimpleDocScraper.py <url>
```
"""
    else:
        report += """**Some components need attention:**

"""
        if test_results['vector_database']['total_chunks'] == 0:
            report += """1. **Populate Vector Database**:
   ```bash
   cd data
   python process_test_data.py
   python build_vector_index.py
   ```

"""
        if not test_results['agent_system']['installed']:
            report += """2. **Install Agent System**:
   ```bash
   cd agents
   ./install.sh
   ```

"""
        if not test_results['mcp_integration']['configured']:
            report += """3. **Configure MCP Integration**:
   - The installer should have created ~/.claude/claude_desktop_config.json
   - Restart Claude Code after configuration

"""
    
    # Add summary
    report += f"""---

## 📈 Installation Summary

- **Overall Success Rate**: {success_rate:.1f}%
- **Vector Database**: {test_results['vector_database']['total_chunks']} chunks indexed
- **Agent System**: {test_results['agent_system']['agents_count']} agents installed
- **Ready for Production**: {'Yes ✅' if success_rate >= 90 else 'No ❌ - See issues above'}

---

*Report generated by Claude Complete Ecosystem Installation Validator*
"""
    
    # Write report
    with open(output_file, 'w') as f:
        f.write(report)
    
    return success_rate

def main():
    """Main function to generate installation report."""
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    home_dir = Path.home()
    
    print("📋 Generating Installation Report")
    print("=" * 50)
    
    # Run all tests
    print("🔍 Testing components...")
    
    test_results = {
        "vector_database": test_vector_database(script_dir / "vector_db"),
        "agent_system": test_agent_system(home_dir),
        "mcp_integration": test_mcp_integration(home_dir),
        "doc_tools": test_doc_tools(project_root / "doc-tools"),
        "vector_server": test_vector_server(project_root / "vector-server")
    }
    
    # Generate report
    report_file = project_root / "INSTALLATION_REPORT.md"
    success_rate = generate_markdown_report(test_results, report_file)
    
    # Console output
    print("\n" + "=" * 50)
    
    if success_rate >= 90:
        print("✅ Installation Successful!")
    elif success_rate >= 70:
        print("⚠️ Installation Partially Successful")
    else:
        print("❌ Installation Failed")
    
    print(f"\n📊 Results:")
    print(f"   • Success Rate: {success_rate:.1f}%")
    print(f"   • Vector DB: {test_results['vector_database']['total_chunks']} chunks")
    print(f"   • Agents: {test_results['agent_system']['agents_count']} installed")
    print(f"   • MCP: {'✅ Configured' if test_results['mcp_integration']['configured'] else '❌ Not configured'}")
    print(f"\n📄 Full report saved to: {report_file}")
    
    return success_rate >= 70

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)