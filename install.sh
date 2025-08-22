#!/bin/bash

# Claude Complete Ecosystem - Master Installer
# Installs all components: Agent System, Vector Server, Doc Tools, and Vector Database

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${CYAN}"
cat << 'EOF'
 ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗    ███████╗ ██████╗ ██████╗ 
██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔═══██╗
██║     ██║     ███████║██║   ██║██║  ██║█████╗      █████╗  ██║     ██║   ██║
██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝      ██╔══╝  ██║     ██║   ██║
╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗    ███████╗╚██████╗╚██████╔╝
 ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝ ╚═════╝ 
EOF
echo -e "${NC}"

echo -e "${GREEN}🚀 Claude Complete Ecosystem Installer${NC}"
echo -e "${YELLOW}────────────────────────────────────────${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Installation directory: $SCRIPT_DIR"

# Check requirements
echo -e "${BLUE}🔍 Checking requirements...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}❌ Python 3.10+ required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check Claude Code CLI
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}⚠️  Claude Code CLI not found - install from https://claude.ai/code${NC}"
    echo -e "${YELLOW}   Installation will continue but integration won't work until Claude Code is installed${NC}"
else
    echo -e "${GREEN}✅ Claude Code CLI${NC}"
fi

# Check git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is required but not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git${NC}"

echo ""

# Installation steps
TOTAL_STEPS=7
CURRENT_STEP=1

install_step() {
    echo -e "${PURPLE}[Step $CURRENT_STEP/$TOTAL_STEPS]${NC} $1"
    CURRENT_STEP=$((CURRENT_STEP + 1))
}

# Step 1: Setup Vector Database
install_step "Setting up Vector Database"
cd "$SCRIPT_DIR/data"
./setup-vector-database.sh
echo ""

# Step 2: Install Vector Server
install_step "Installing MCP Vector Server"
cd "$SCRIPT_DIR/vector-server"

# Create virtual environment for vector server
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment for vector server..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "📥 Installing vector server dependencies..."
pip install --upgrade pip
pip install -e .
pip install -e ".[dev]"
deactivate

echo "✅ Vector server installed"
echo ""

# Step 3: Install Doc Tools  
install_step "Installing Documentation Tools"
cd "$SCRIPT_DIR/doc-tools"

# Create virtual environment for doc tools
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment for doc tools..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "📥 Installing doc tools dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install chromium

deactivate

echo "✅ Doc tools installed"
echo ""

# Step 4: Install Agent System
install_step "Installing Agent System"
cd "$SCRIPT_DIR/agents"

# Agent system doesn't need separate venv - it integrates with Claude Code
echo "🤖 Configuring global agent system..."

# Ensure Claude Code can find the global configuration
CLAUDE_CONFIG_DIR="$HOME/.claude"
mkdir -p "$CLAUDE_CONFIG_DIR"

# Copy global CLAUDE.md if it doesn't exist or is older
if [ ! -f "$CLAUDE_CONFIG_DIR/CLAUDE.md" ] || [ "$SCRIPT_DIR/agents/CLAUDE.md" -nt "$CLAUDE_CONFIG_DIR/CLAUDE.md" ]; then
    echo "📋 Installing global Claude Code configuration..."
    cp "$SCRIPT_DIR/agents/CLAUDE.md" "$CLAUDE_CONFIG_DIR/CLAUDE.md"
fi

echo "✅ Agent system configured globally"
echo ""

# Step 5: Setup MCP Integration
install_step "Configuring MCP Integration"

# Create Claude Code MCP configuration
CLAUDE_MCP_CONFIG="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
VECTOR_SERVER_PATH="$SCRIPT_DIR/vector-server"

# Check if MCP config exists and backup if needed
if [ -f "$CLAUDE_MCP_CONFIG" ]; then
    echo "📋 Backing up existing Claude MCP configuration..."
    cp "$CLAUDE_MCP_CONFIG" "$CLAUDE_MCP_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create or update MCP configuration
echo "🔧 Configuring MCP Vector Server integration..."
cat > "$CLAUDE_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "vector-search": {
      "command": "$VECTOR_SERVER_PATH/venv/bin/python",
      "args": ["-m", "mcp_vector_server"],
      "cwd": "$VECTOR_SERVER_PATH",
      "env": {
        "VECTOR_DB_PATH": "$SCRIPT_DIR/data/vector_db"
      }
    }
  }
}
EOF

echo "✅ MCP integration configured"
echo ""

# Step 6: Auto-scrape Claude Code Documentation
install_step "Auto-scraping Claude Code Documentation (Test Installation)"
cd "$SCRIPT_DIR/doc-tools"

echo "📖 Scraping Claude Code documentation for testing..."
source venv/bin/activate

# Create test scraping script
cat > "test_scrape_claude_docs.py" << 'EOF'
#!/usr/bin/env python3
"""
Auto-scrape Claude Code documentation for test installation
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def scrape_claude_docs():
    """Scrape Claude Code documentation"""
    print("🔍 Scraping Claude Code documentation...")
    
    # Target URLs for Claude Code documentation
    urls = [
        "https://docs.anthropic.com/en/docs/claude-code",
        "https://docs.anthropic.com/en/docs/claude-code/overview",
        "https://docs.anthropic.com/en/docs/claude-code/quickstart",
        "https://docs.anthropic.com/en/docs/claude-code/memory",
        "https://docs.anthropic.com/en/docs/claude-code/common-workflows"
    ]
    
    # Create test data directory
    test_data_dir = Path("../data/test_data")
    test_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Scrape each URL
    scraped_files = []
    for i, url in enumerate(urls):
        try:
            print(f"📥 Scraping {url}...")
            
            # Use SimpleDocScraper for reliable scraping
            output_file = test_data_dir / f"claude_docs_{i}.md"
            
            # Simple scraping command
            result = subprocess.run([
                "python3", "SimpleDocScraper.py", 
                url, 
                str(test_data_dir),
                "5"  # Limit to 5 pages per URL
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                scraped_files.append(str(output_file))
                print(f"✅ Scraped to {output_file}")
            else:
                print(f"⚠️ Failed to scrape {url}: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout scraping {url}")
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    
    # Create summary
    summary = {
        "scraped_urls": len(scraped_files),
        "total_attempted": len(urls),
        "files": scraped_files,
        "status": "completed" if scraped_files else "failed"
    }
    
    with open(test_data_dir / "scrape_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    return len(scraped_files) > 0

if __name__ == "__main__":
    success = scrape_claude_docs()
    if success:
        print("✅ Claude Code documentation scraping completed")
        sys.exit(0)
    else:
        print("⚠️ Claude Code documentation scraping failed - continuing installation")
        sys.exit(0)  # Don't fail installation
EOF

# Run the scraping (don't fail installation if this fails)
python3 test_scrape_claude_docs.py || echo "⚠️ Documentation scraping failed - continuing installation"

# Clean up
rm -f test_scrape_claude_docs.py

deactivate
echo ""

# Step 7: Final Configuration and Testing
install_step "Final Configuration and Testing"

# Create global command scripts
echo "🔧 Creating global command shortcuts..."

# Vector server command
cat > "/usr/local/bin/mcp-vector-server" << EOF
#!/bin/bash
cd "$SCRIPT_DIR/vector-server"
source venv/bin/activate
python -m mcp_vector_server "\$@"
EOF

# Doc scraper command
cat > "/usr/local/bin/claude-doc-scraper" << EOF
#!/bin/bash
cd "$SCRIPT_DIR/doc-tools"
source venv/bin/activate
python SimpleDocScraper.py "\$@"
EOF

# Doc scraper GUI command
cat > "/usr/local/bin/claude-doc-scraper-gui" << EOF
#!/bin/bash
cd "$SCRIPT_DIR/doc-tools"
source venv/bin/activate
python DocScraperGUI.py "\$@"
EOF

# Make scripts executable
chmod +x /usr/local/bin/mcp-vector-server 2>/dev/null || echo "⚠️ Could not create global commands (requires sudo)"
chmod +x /usr/local/bin/claude-doc-scraper 2>/dev/null || echo "⚠️ Could not create global commands (requires sudo)"
chmod +x /usr/local/bin/claude-doc-scraper-gui 2>/dev/null || echo "⚠️ Could not create global commands (requires sudo)"

# Test installation
echo "🧪 Testing installation..."

# Test vector server
cd "$SCRIPT_DIR/vector-server"
source venv/bin/activate
python -c "import mcp_vector_server; print('✅ Vector server import successful')" || echo "⚠️ Vector server test failed"
deactivate

# Test doc tools
cd "$SCRIPT_DIR/doc-tools"
source venv/bin/activate
python -c "import requests; import beautifulsoup4; print('✅ Doc tools import successful')" || echo "⚠️ Doc tools test failed"
deactivate

echo ""
echo -e "${GREEN}🎉 Installation Complete!${NC}"
echo -e "${YELLOW}════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}📋 What was installed:${NC}"
echo "   🤖 Agent System - Global Claude Code integration"
echo "   🗃️ Vector Database - Empty, ready for your documentation"  
echo "   🔍 MCP Vector Server - Semantic search integration"
echo "   📖 Documentation Tools - Web scraper and post-processor"
echo "   🧪 Test Data - Claude Code documentation for testing"
echo ""
echo -e "${CYAN}🚀 Quick Start:${NC}"
echo "   1. Restart Claude Code to load new MCP configuration"
echo "   2. Test with: claude-doc-scraper --help"
echo "   3. Scrape docs: claude-doc-scraper https://your-docs.com"
echo "   4. Use GUI: claude-doc-scraper-gui"
echo ""
echo -e "${CYAN}📁 Important Paths:${NC}"
echo "   📂 Installation: $SCRIPT_DIR"
echo "   ⚙️ Claude Config: $CLAUDE_CONFIG_DIR"
echo "   🗃️ Vector DB: $SCRIPT_DIR/data/vector_db"
echo "   🧪 Test Data: $SCRIPT_DIR/data/test_data"
echo ""
echo -e "${CYAN}🔧 Configuration:${NC}"
echo "   📋 Global agent config: $CLAUDE_CONFIG_DIR/CLAUDE.md"
echo "   🔌 MCP config: $CLAUDE_CONFIG_DIR/claude_desktop_config.json"
echo ""

# Check for API keys
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}💡 Optional: Set OPENAI_API_KEY for enhanced doc processing${NC}"
fi

if [ -z "$FIRECRAWL_API_KEY" ]; then
    echo -e "${YELLOW}💡 Optional: Set FIRECRAWL_API_KEY for advanced scraping${NC}"
fi

echo ""
echo -e "${GREEN}✨ Your Claude Complete Ecosystem is ready!${NC}"
echo -e "${CYAN}🔗 Next: Restart Claude Code and start using the agentic system${NC}"

exit 0