#!/bin/bash

# Firecrawl MCP Setup Script
# This script configures the Firecrawl MCP server using the API key from .env file

echo "🔧 Setting up Firecrawl MCP Server..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    if [ -f "example.env" ]; then
        echo "📋 Found example.env file. Would you like to copy it to .env? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            cp example.env .env
            echo "✅ Copied example.env to .env"
            echo "📝 Please edit .env and add your actual Firecrawl API key"
            echo "   Get your API key from: https://firecrawl.dev"
            echo ""
            echo "After editing .env, run this script again."
            exit 0
        fi
    fi
    echo ""
    echo "Please create a .env file with your Firecrawl API key:"
    echo "  cp example.env .env"
    echo "  # Edit .env with your actual API key"
    echo "  # Get API key from: https://firecrawl.dev"
    exit 1
fi

# Extract API key from .env file
API_KEY=$(grep "firecrawl-api-key" .env | cut -d'=' -f2)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "your-firecrawl-api-key-here" ]; then
    echo "❌ Error: No valid Firecrawl API key found in .env file!"
    echo ""
    echo "Please edit your .env file and replace the placeholder with your actual API key:"
    echo "  firecrawl-api-key=fc-your-actual-api-key-here"
    echo ""
    echo "Get your API key from: https://firecrawl.dev"
    exit 1
fi

echo "✅ Found Firecrawl API key in .env file"
echo ""

# Test the API key format
if [[ $API_KEY =~ ^fc-[a-zA-Z0-9]{32}$ ]]; then
    echo "✅ API key format is valid"
else
    echo "⚠️  Warning: API key format may be invalid"
    echo "Expected format: fc-xxxxxxxxxxxxxxxxxxxxxxxxx"
fi

echo ""
echo "🚀 Adding Firecrawl MCP server to Claude configuration..."

# Add MCP server to Claude configuration
claude mcp add firecrawl "env FIRECRAWL_API_KEY=$API_KEY npx -y @mendable/firecrawl-mcp"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Firecrawl MCP server configured successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Restart Claude Code to pick up the new MCP configuration"
    echo "2. Test the research agent functionality"
    echo "3. The research agent will now have access to Firecrawl tools"
    echo ""
    echo "🔒 Security: Your API key is stored securely in .env file (gitignored)"
else
    echo ""
    echo "❌ Failed to configure Firecrawl MCP server"
    echo "Please check your Claude Code installation and try again"
fi 