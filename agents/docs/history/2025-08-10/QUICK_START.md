> Archived on 2025-08-10. Replaced by `docs/dev-setup.md` and `docs/overview.md`.
> Consolidated to reduce duplication and keep a single source of truth.

---

### Original content (for history)

# 🚀 Quick Start - Claude Code Agent System

## 30-Second Setup

```bash
# Clone
git clone https://github.com/[your-username]/claude-code-agent-system.git
cd claude-code-agent-system

# Configure (for research-agent MCP functionality)
cp example.env .env
# Edit .env with your Firecrawl API key from https://firecrawl.dev

# Install
./install.sh

# Setup MCP
./setup-firecrawl-mcp.sh

# Verify
/agents  # In Claude Code
```

## What You Get

✅ **8 Specialized Agents** - Ready to use globally across all projects  
✅ **Automatic Learning** - Improvement Agent starts with your first prompt  
✅ **Continuous Evolution** - System gets smarter with each project  
✅ **Zero Configuration** - Works immediately after installation  

## GitHub Repository Setup

1. Create a new repository on GitHub named `claude-code-agent-system`
2. Push your local repository:

```bash
cd ~/Desktop/claude-code-agent-system
git remote add origin https://github.com/[your-username]/claude-code-agent-system.git
git branch -M main
git push -u origin main
```

## Using on Other Devices

Simply clone and install:
```bash
git clone https://github.com/[your-username]/claude-code-agent-system.git
cd claude-code-agent-system
./install.sh
```

## The Magic Happens Automatically

1. **Start any project** - Improvement Agent activates
2. **Work normally** - Agents coordinate seamlessly  
3. **Finish project** - System analyzes and improves
4. **Each project** - Makes all agents smarter

## Need Help?

- Check [SETUP.md](SETUP.md) for detailed instructions
- Read [README.md](README.md) for system overview
- Review agent files in `agents/` for capabilities

---

💡 **Remember**: The system is always learning. Every project makes it better!