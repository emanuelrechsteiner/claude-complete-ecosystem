> Archived on 2025-08-10. Replaced by `docs/dev-setup.md`.
> Consolidated to reduce duplication and keep a single source of truth.

---

### Original content (for history)

# Setup Guide - Claude Code Multi-Agent System

## Quick Start

### 1. Clone and Install
```bash
# Clone the repository
git clone https://github.com/[your-username]/claude-code-agent-system.git
cd claude-code-agent-system

# Configure environment variables
cp example.env .env
# Edit .env with your actual API keys (see Environment Configuration section below)

# Run installer
./install.sh

# Set up Firecrawl MCP for research-agent
./setup-firecrawl-mcp.sh
```

### 2. Verify Installation
After installation, you can verify everything is working:

```bash
# Check if agents are installed
ls ~/.claude/agents/

# In Claude Code, use the /agents command
/agents
```

You should see all 8 agents listed.

## Environment Configuration

### Setting Up API Keys

The system uses environment variables for secure API key management. This enables the research agent to use MCP servers for documentation scraping.

#### 1. Copy Environment Template
```bash
cp example.env .env
```

#### 2. Edit Environment Variables
Open `.env` in your preferred editor and replace the placeholder values:

```bash
# Required for research-agent
firecrawl-api-key=fc-your-actual-firecrawl-api-key-here

# Optional: Add other API keys as needed
# openai-api-key=your-openai-api-key-here
# anthropic-api-key=your-anthropic-api-key-here
```

#### 3. Get Firecrawl API Key
1. Visit [Firecrawl.dev](https://firecrawl.dev)
2. Sign up for an account
3. Navigate to your dashboard
4. Copy your API key (format: `fc-xxxxxxxxxxxxxxxxxxxxxxxxx`)
5. Paste it in your `.env` file

#### 4. Run MCP Setup
```bash
./setup-firecrawl-mcp.sh
```

This script will:
- Validate your API key format
- Configure the Firecrawl MCP server in Claude Code
- Provide setup verification

#### 5. Restart Claude Code
After MCP configuration, restart Claude Code to pick up the new server.

### Security Notes
- `.env` file is automatically gitignored for security
- Never commit API keys to version control
- Keep your API keys private and secure
- The setup script validates API key format before configuration

### Testing Research Agent
After setup, test the research agent:
```
"Research React 19 new features for our project"
```

The research agent should now have access to Firecrawl tools for documentation scraping.

## Multi-Device Setup

To use this system across multiple devices:

### On Your Primary Device (where you set it up):
1. Push to GitHub:
```bash
cd ~/Desktop/claude-code-agent-system
git add .
git commit -m "Initial agent system setup"
git remote add origin https://github.com/[your-username]/claude-code-agent-system.git
git push -u origin main
```

### On Other Devices:
1. Clone and install:
```bash
git clone https://github.com/[your-username]/claude-code-agent-system.git
cd claude-code-agent-system
./install.sh
```

2. The global observation ledger will start fresh on each device but will accumulate device-specific learnings.

### Syncing Learnings (Optional)
If you want to sync learnings between devices, you can periodically:

```bash
# On device with learnings to share
cp ~/.claude/global-observation/observation-ledger.json ~/Desktop/claude-code-agent-system/global-observation/
cd ~/Desktop/claude-code-agent-system
git add global-observation/observation-ledger.json
git commit -m "Update global observations"
git push

# On other devices
cd ~/Desktop/claude-code-agent-system
git pull
cp global-observation/observation-ledger.json ~/.claude/global-observation/
```

## How the System Works

### Automatic Activation
1. **Start any project** in Claude Code
2. The **Improvement Agent** activates automatically with your first prompt
3. It observes silently throughout your project
4. Data is saved to the global ledger

### Agent Coordination
- **Planning Agent** creates strategic plans
- **Control Agent** ensures quality
- **Specialized Agents** handle specific tasks
- **Improvement Agent** learns continuously

### Post-Project Analysis
When a project completes:
1. Control Agent activates the Improvement Agent's Meta Layer
2. Deep analysis using Claude Opus 4
3. Generates improvement recommendations
4. Requires approval before implementing

## Customization

### Modifying Agents
Edit agent files in `~/.claude/agents/`:
```bash
# Example: Add a new tool to UI Agent
vi ~/.claude/agents/ui-agent.md
# Edit the tools: line in YAML frontmatter
```

### Adding New Agents
1. Create a new `.md` file in `~/.claude/agents/`
2. Add YAML frontmatter:
```yaml
---
name: my-new-agent
description: What this agent does
tools: ["Read", "Write", "Edit"]
---

Your agent's system prompt and instructions here...
```

## Troubleshooting

### Agents Not Showing
1. Restart Claude Code
2. Check installation:
```bash
ls -la ~/.claude/agents/
```
3. Ensure files have `.md` extension
4. Verify YAML frontmatter is valid

### Observation Not Working
1. Check global ledger exists:
```bash
ls -la ~/.claude/global-observation/
```
2. Verify write permissions:
```bash
ls -la ~/.claude/ | grep global-observation
```

### Reset System
To start fresh:
```bash
./uninstall.sh
./install.sh
```

## Best Practices

### For Maximum Learning
1. Let projects run to completion
2. Allow Control Agent to trigger analysis
3. Review and approve meaningful improvements
4. The system gets smarter with each project

### For Multi-Device Use
1. Commit observation data periodically
2. Pull updates before starting work
3. Consider device-specific branches for testing

### For Team Use
1. Fork the repository for your team
2. Customize agents for your workflow
3. Share improvements via pull requests
4. Maintain a central observation ledger

## Data Privacy

- All data stored locally in `~/.claude/`
- No automatic cloud sync
- You control what goes to GitHub
- Observation data can be excluded via `.gitignore`

## Support

- Check the [README](README.md) for overview
- Review agent files for specific capabilities
- Submit issues on GitHub for problems
- Share improvements with the community