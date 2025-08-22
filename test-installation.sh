#!/bin/bash

# Claude Complete Ecosystem - Installation Test Suite
# Comprehensive testing of all components and integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🧪 Claude Complete Ecosystem Test Suite${NC}"
echo -e "${YELLOW}═══════════════════════════════════════${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAILED_TESTS=0
PASSED_TESTS=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${BLUE}🔍 Testing: ${NC}$test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Test function with output
run_test_with_output() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${BLUE}🔍 Testing: ${NC}$test_name"
    
    if output=$(eval "$test_command" 2>&1); then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        if [ -n "$output" ]; then
            echo -e "${YELLOW}   Output: ${NC}$output"
        fi
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        if [ -n "$output" ]; then
            echo -e "${RED}   Error: ${NC}$output"
        fi
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

echo -e "${PURPLE}[1/6]${NC} Basic System Tests"
echo "────────────────────────"

# Test Python
run_test "Python 3.10+ available" "python3 -c 'import sys; assert sys.version_info >= (3, 10)'"

# Test directory structure
run_test "Agent system directory exists" "[ -d '$SCRIPT_DIR/agents' ]"
run_test "Vector server directory exists" "[ -d '$SCRIPT_DIR/vector-server' ]"
run_test "Doc tools directory exists" "[ -d '$SCRIPT_DIR/doc-tools' ]"
run_test "Vector database directory exists" "[ -d '$SCRIPT_DIR/data/vector_db' ]"

# Test configuration files
run_test "Database configuration exists" "[ -f '$SCRIPT_DIR/data/vector_db/config/database.json' ]"
run_test "Vector server pyproject.toml exists" "[ -f '$SCRIPT_DIR/vector-server/pyproject.toml' ]"
run_test "Doc tools requirements.txt exists" "[ -f '$SCRIPT_DIR/doc-tools/requirements.txt' ]"

echo ""
echo -e "${PURPLE}[2/6]${NC} Virtual Environment Tests"
echo "─────────────────────────────"

# Test vector server venv
run_test "Vector server virtual environment exists" "[ -d '$SCRIPT_DIR/vector-server/venv' ]"
if [ -d "$SCRIPT_DIR/vector-server/venv" ]; then
    run_test "Vector server venv activation" "source '$SCRIPT_DIR/vector-server/venv/bin/activate' && python -c 'import sys; print(sys.prefix)' && deactivate"
fi

# Test doc tools venv
run_test "Doc tools virtual environment exists" "[ -d '$SCRIPT_DIR/doc-tools/venv' ]"
if [ -d "$SCRIPT_DIR/doc-tools/venv" ]; then
    run_test "Doc tools venv activation" "source '$SCRIPT_DIR/doc-tools/venv/bin/activate' && python -c 'import sys; print(sys.prefix)' && deactivate"
fi

echo ""
echo -e "${PURPLE}[3/6]${NC} Dependency Tests"
echo "───────────────────"

# Test vector server dependencies
if [ -d "$SCRIPT_DIR/vector-server/venv" ]; then
    cd "$SCRIPT_DIR/vector-server"
    source venv/bin/activate
    
    run_test "MCP library installed" "python -c 'import mcp'"
    run_test "Sentence transformers installed" "python -c 'import sentence_transformers'"
    run_test "Numpy installed" "python -c 'import numpy'"
    run_test "Scikit-learn installed" "python -c 'import sklearn'"
    run_test "Pydantic installed" "python -c 'import pydantic'"
    
    deactivate
fi

# Test doc tools dependencies
if [ -d "$SCRIPT_DIR/doc-tools/venv" ]; then
    cd "$SCRIPT_DIR/doc-tools"
    source venv/bin/activate
    
    run_test "BeautifulSoup4 installed" "python -c 'import bs4'"
    run_test "Requests installed" "python -c 'import requests'"
    run_test "Playwright installed" "python -c 'import playwright'"
    run_test "OpenAI installed" "python -c 'import openai'"
    
    deactivate
fi

echo ""
echo -e "${PURPLE}[4/6]${NC} Component Functionality Tests"
echo "────────────────────────────────"

# Test vector server functionality
if [ -d "$SCRIPT_DIR/vector-server/venv" ]; then
    cd "$SCRIPT_DIR/vector-server"
    source venv/bin/activate
    
    run_test_with_output "Vector server module import" "python -c 'import mcp_vector_server; print(\"Vector server module imported successfully\")'"
    run_test_with_output "Vector server models import" "python -c 'from mcp_vector_server.models import DocumentChunk; print(\"Models imported successfully\")'"
    
    deactivate
fi

# Test doc tools functionality  
if [ -d "$SCRIPT_DIR/doc-tools/venv" ]; then
    cd "$SCRIPT_DIR/doc-tools"
    source venv/bin/activate
    
    run_test "Simple doc scraper exists" "[ -f 'SimpleDocScraper.py' ]"
    run_test "Doc post processor exists" "[ -f 'DocPostProcessor.py' ]"
    run_test "GUI scripts exist" "[ -f 'DocScraperGUI.py' ] && [ -f 'DocPostProcessorGUI.py' ]"
    
    deactivate
fi

echo ""
echo -e "${PURPLE}[5/6]${NC} Integration Tests"
echo "────────────────────"

# Test Claude Code configuration
CLAUDE_CONFIG_DIR="$HOME/.claude"
run_test "Claude config directory exists" "[ -d '$CLAUDE_CONFIG_DIR' ]"
run_test "Global CLAUDE.md exists" "[ -f '$CLAUDE_CONFIG_DIR/CLAUDE.md' ]"
run_test "MCP configuration exists" "[ -f '$CLAUDE_CONFIG_DIR/claude_desktop_config.json' ]"

# Test MCP configuration content
if [ -f "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" ]; then
    run_test "MCP config contains vector-search" "grep -q 'vector-search' '$CLAUDE_CONFIG_DIR/claude_desktop_config.json'"
fi

# Test vector database structure
run_test "Vector DB chunks directory" "[ -d '$SCRIPT_DIR/data/vector_db/chunks' ]"
run_test "Vector DB embeddings directory" "[ -d '$SCRIPT_DIR/data/vector_db/embeddings' ]"
run_test "Vector DB metadata directory" "[ -d '$SCRIPT_DIR/data/vector_db/metadata' ]"
run_test "Vector DB indices directory" "[ -d '$SCRIPT_DIR/data/vector_db/indices' ]"

echo ""
echo -e "${PURPLE}[6/6]${NC} Test Data and Auto-Scraping Tests"
echo "─────────────────────────────────────"

# Test for test data
run_test "Test data directory exists" "[ -d '$SCRIPT_DIR/data/test_data' ]"

# Check if Claude docs were scraped
TEST_DATA_COUNT=0
if [ -d "$SCRIPT_DIR/data/test_data" ]; then
    TEST_DATA_COUNT=$(find "$SCRIPT_DIR/data/test_data" -name "*.md" | wc -l)
fi

if [ "$TEST_DATA_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}: Claude Code documentation auto-scraping ($TEST_DATA_COUNT files)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${YELLOW}⚠️ SKIP${NC}: Claude Code documentation auto-scraping (no files found)"
fi

# Test global commands (if they were created successfully)
if command -v mcp-vector-server &> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: Global mcp-vector-server command available"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${YELLOW}⚠️ SKIP${NC}: Global mcp-vector-server command (may require sudo)"
fi

if command -v claude-doc-scraper &> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: Global claude-doc-scraper command available"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${YELLOW}⚠️ SKIP${NC}: Global claude-doc-scraper command (may require sudo)"
fi

echo ""
echo -e "${CYAN}📊 Test Results${NC}"
echo "═══════════════"
echo -e "${GREEN}✅ Passed: $PASSED_TESTS${NC}"
echo -e "${RED}❌ Failed: $FAILED_TESTS${NC}"

TOTAL_TESTS=$((PASSED_TESTS + FAILED_TESTS))
if [ $TOTAL_TESTS -gt 0 ]; then
    SUCCESS_RATE=$(( (PASSED_TESTS * 100) / TOTAL_TESTS ))
    echo -e "${BLUE}📈 Success Rate: $SUCCESS_RATE%${NC}"
fi

echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Installation is successful.${NC}"
    echo ""
    echo -e "${CYAN}🚀 Ready to use:${NC}"
    echo "   • Agent system is configured globally"
    echo "   • MCP Vector Server is ready"
    echo "   • Documentation tools are available"
    echo "   • Vector database is initialized"
    echo ""
    echo -e "${CYAN}💡 Next steps:${NC}"
    echo "   1. Restart Claude Code to load MCP configuration"
    echo "   2. Test scraping: claude-doc-scraper https://docs.example.com"
    echo "   3. The agent system will work automatically in Claude Code"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please check the installation.${NC}"
    echo ""
    echo -e "${CYAN}🔧 Troubleshooting:${NC}"
    echo "   • Re-run ./install.sh to fix missing components"
    echo "   • Check Python version (3.10+ required)"
    echo "   • Ensure stable internet connection"
    echo "   • Verify disk space is available"
    exit 1
fi