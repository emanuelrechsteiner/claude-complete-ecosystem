# Troubleshooting Guide

## Quick Diagnostics

### System Health Check
Run these commands to verify system status:

```bash
# Check installation
ls -la ~/.claude/agents/ | head -5
ls -la ~/.claude/ledgers/ | head -5
ls -la ~/.claude/templates/

# In Claude Code
/agents  # Should show 12 agents

# Test basic agent
"What agents are available?"

# Test complex coordination
"Use the control-agent to coordinate a simple task"
```

## Common Installation Issues

### Issue: Installation Script Fails

#### Symptoms
- `./install.sh` returns errors
- Permission denied messages
- Directory creation fails

#### Solutions

1. **Check permissions**:
```bash
chmod +x install.sh
chmod +x setup-firecrawl-mcp.sh
chmod +x uninstall.sh
```

2. **Run with proper shell**:
```bash
bash install.sh  # Instead of ./install.sh
```

3. **Manual installation**:
```bash
# Create directories manually
mkdir -p ~/.claude/{agents,global-observation,ledgers,observation,templates}

# Copy files manually
cp -r agents/* ~/.claude/agents/
cp -r templates/* ~/.claude/templates/
cp -r ledgers/* ~/.claude/ledgers/
```

### Issue: Agents Not Appearing

#### Symptoms
- `/agents` shows fewer than 12 agents
- "Agent not found" errors
- Agents not responding to invocation

#### Solutions

1. **Verify installation**:
```bash
# Count installed agents
ls -1 ~/.claude/agents/*.md | wc -l  # Should be 12+

# List agent files
ls ~/.claude/agents/
```

2. **Check agent file format**:
```bash
# Verify YAML frontmatter
head -20 ~/.claude/agents/control-agent.md
```

3. **Restart Claude Code**:
- Completely quit Claude Code
- Reopen and test with `/agents`

4. **Reinstall agents**:
```bash
cd /path/to/claude-code-agent-system
./uninstall.sh
./install.sh
```

### Issue: MCP Configuration Problems

#### Symptoms
- Research agent not working
- "Firecrawl not configured" errors
- MCP tools unavailable

#### Solutions

1. **Verify API key**:
```bash
# Check if .env exists
cat .env | grep firecrawl

# Ensure key format is correct (fc-...)
```

2. **Run MCP setup**:
```bash
./setup-firecrawl-mcp.sh
```

3. **Check MCP configuration**:
```bash
# Verify MCP config exists
ls ~/.config/claude/mcp/
```

4. **Test Firecrawl directly**:
```text
"Research React 19 features using Firecrawl"
```

## Agent Coordination Problems

### Issue: Control Agent Not Delegating

#### Symptoms
- Control agent tries to do everything itself
- No delegation to specialized agents
- Workflow not triggering

#### Solutions

1. **Force delegation pattern**:
```text
"Control-agent, delegate this task to the appropriate specialized agents: [task description]"
```

2. **Check CLAUDE.md is loaded**:
```text
"Show me the current workflow rules from CLAUDE.md"
```

3. **Explicitly invoke workflow**:
```text
"Following the mandatory workflow, coordinate building [feature]"
```

### Issue: Agents Not Reporting

#### Symptoms
- No progress updates from agents
- Agents working silently
- Missing coordination between agents

#### Solutions

1. **Request status explicitly**:
```text
"All agents, report your current status"
```

2. **Check ledger updates**:
```bash
# Monitor ledger files for changes
ls -la ~/.claude/ledgers/*.json
```

3. **Force reporting protocol**:
```text
"Backend-agent, report to control-agent before starting work on [task]"
```

### Issue: Commit Frequency Violations

#### Symptoms
- Agents not committing within 60 minutes
- Large uncommitted changes
- Lost work due to no commits

#### Solutions

1. **Set explicit reminders**:
```text
"All agents must commit every 30 minutes. Set this as a requirement."
```

2. **Monitor git status**:
```bash
git status
git diff --stat
```

3. **Force immediate commit**:
```text
"Version-control-agent, commit all current work immediately"
```

## Bootstrap Command Issues

### Issue: Bootstrap Not Recognized

#### Symptoms
- `/bootstrap` returns "command not found"
- Slash command not available
- Bootstrap features missing

#### Solutions

1. **Verify command installation**:
```bash
ls ~/.claude/commands/
cat ~/.claude/commands/bootstrap.md | head -10
```

2. **Reinstall with bootstrap support**:
```bash
# Ensure latest version
git pull origin main

# Reinstall
./install.sh
```

3. **Manual command test**:
```text
"Import @~/.claude/commands/bootstrap.md and execute"
```

### Issue: Bootstrap Fails to Create Files

#### Symptoms
- No files created after bootstrap
- "Permission denied" errors
- Incomplete bootstrap execution

#### Solutions

1. **Check permissions**:
```bash
# Verify write permissions
touch test.md && rm test.md

# Check directory permissions
ls -la .
```

2. **Run with explicit approval**:
```text
/bootstrap --yes --docs-only
```

3. **Try incremental bootstrap**:
```text
# Start with read-only
/bootstrap --docs-only

# Then proceed if successful
/bootstrap --bootstrap-only
```

### Issue: Templates Not Found

#### Symptoms
- "Template not found" errors
- Empty CLAUDE.md generation
- Missing agent configurations

#### Solutions

1. **Verify templates exist**:
```bash
ls ~/.claude/templates/bootstrap/
ls ~/.claude/templates/bootstrap/agents/
```

2. **Reinstall templates**:
```bash
cp -r templates/* ~/.claude/templates/
```

3. **Check template syntax**:
```bash
# Verify template files are valid
cat ~/.claude/templates/bootstrap/CLAUDE.md | head -20
```

## Hook Execution Problems

### Issue: Hooks Not Running

#### Symptoms
- Auto-format not working
- Safety checks not triggered
- Hooks silently failing

#### Solutions

1. **Check hook permissions**:
```bash
chmod +x .claude/hooks/*.sh
ls -la .claude/hooks/
```

2. **Test hooks manually**:
```bash
bash .claude/hooks/auto-format.sh
bash .claude/hooks/guard-unsafe.sh
```

3. **Verify hook configuration**:
```bash
cat .claude/settings.json | jq .hooks
```

### Issue: Hook Errors

#### Symptoms
- Error messages during operations
- Hooks blocking normal workflow
- Unexpected behavior

#### Solutions

1. **Debug hook execution**:
```bash
bash -x .claude/hooks/auto-format.sh  # Debug mode
```

2. **Check hook dependencies**:
```bash
# Ensure required tools exist
which prettier
which black
which gofmt
```

3. **Disable problematic hooks temporarily**:
```json
// .claude/settings.json
{
  "hooks": {
    // "pre-commit": ".claude/hooks/auto-format.sh"
  }
}
```

## Performance Issues

### Issue: Slow Agent Response

#### Symptoms
- Long delays before agent responds
- Timeouts during operations
- System feels sluggish

#### Solutions

1. **Check system resources**:
```bash
# Monitor CPU and memory
top
df -h  # Disk space
```

2. **Clear cached data**:
```bash
# Clear old ledger entries
# Backup first!
cp -r ~/.claude/ledgers ~/.claude/ledgers.backup
# Then clean old entries
```

3. **Optimize agent invocation**:
```text
# Be specific about agent and task
"UI-agent, implement only the login component"
# Instead of
"Build the entire authentication system"
```

### Issue: Memory/Context Limits

#### Symptoms
- "Context too large" errors
- Agents forgetting previous work
- Incomplete responses

#### Solutions

1. **Break down tasks**:
```text
# Split into smaller chunks
"First, implement the backend API"
"Next, create the frontend components"
"Finally, add tests"
```

2. **Clear unnecessary context**:
```text
"Focus only on the current file: [filename]"
```

3. **Use targeted agents**:
```text
# Specific agent for specific task
"Documentation-agent, update only the API docs"
```

## Git and Version Control Issues

### Issue: Commit Failures

#### Symptoms
- "Nothing to commit" when changes exist
- Pre-commit hooks failing
- Commits not creating

#### Solutions

1. **Check git status**:
```bash
git status
git diff
```

2. **Stage changes properly**:
```bash
git add -A
git status
```

3. **Bypass hooks if needed**:
```bash
git commit --no-verify -m "Emergency commit"
```

### Issue: Branch Conflicts

#### Symptoms
- Merge conflicts during agent work
- Agents overwriting each other's changes
- Lost work due to conflicts

#### Solutions

1. **Coordinate through control-agent**:
```text
"Control-agent, ensure agents work on separate files"
```

2. **Use feature branches**:
```bash
git checkout -b feature/agent-work
```

3. **Regular synchronization**:
```text
"Version-control-agent, sync with main branch"
```

## Debug Mode and Logging

### Enable Verbose Output

1. **Set environment variables**:
```bash
export LOG_LEVEL=debug
export MCP_DEBUG=true
```

2. **Use verbose flags**:
```text
/bootstrap --docs-only  # Start with read-only
```

3. **Monitor log files**:
```bash
# If logs are available
tail -f ~/.claude/logs/*.log
```

### Diagnostic Information Collection

When reporting issues, collect:

```bash
# System info
echo "OS: $(uname -a)"
echo "Claude Code version: [check in app]"
echo "Agents installed: $(ls -1 ~/.claude/agents/*.md | wc -l)"

# Recent activity
ls -lat ~/.claude/ledgers/ | head -5
ls -lat ~/.claude/global-observation/ | head -5

# Git status
git status
git log --oneline -5

# Error messages (if any)
# Copy exact error text
```

## Recovery Procedures

### Complete System Reset

```bash
# 1. Backup current state
cp -r ~/.claude ~/.claude.backup.$(date +%Y%m%d)

# 2. Uninstall
./uninstall.sh

# 3. Clean install
./install.sh

# 4. Reconfigure
cp example.env .env
# Edit .env with your API keys

# 5. Setup MCP
./setup-firecrawl-mcp.sh

# 6. Test
# In Claude Code: /agents
```

### Partial Reset (Keep Data)

```bash
# Keep ledgers and observations
cp -r ~/.claude/ledgers /tmp/ledgers.backup
cp -r ~/.claude/global-observation /tmp/global.backup

# Reinstall
./uninstall.sh
./install.sh

# Restore data
cp -r /tmp/ledgers.backup/* ~/.claude/ledgers/
cp -r /tmp/global.backup/* ~/.claude/global-observation/
```

## Getting Help

### Self-Help Resources

1. **Check documentation**:
   - [Overview](./overview.md) - System overview
   - [Architecture](./architecture.md) - System design
   - [Agent Reference](./agent-reference.md) - Agent capabilities
   - [Bootstrap Guide](./bootstrap-guide.md) - Project setup

2. **Test minimal scenarios**:
   ```text
   # Test basic agent
   "Hello, testing agent system"
   
   # Test specific agent
   "Documentation-agent, are you available?"
   ```

3. **Review recent changes**:
   ```bash
   git log --oneline -10
   git diff HEAD~1
   ```

### Community Support

1. **GitHub Issues**:
   - Search existing issues first
   - Provide diagnostic information
   - Include reproduction steps

2. **Discussion Forums**:
   - Claude Code community
   - Agent system discussions

3. **Direct Support**:
   - For critical issues, check repository README for contact information

## Preventive Maintenance

### Daily Checks
- Verify agents respond: `/agents`
- Check git status for uncommitted work
- Review ledger updates

### Weekly Maintenance
- Clean old ledger entries
- Update documentation
- Review and commit observation data

### Monthly Updates
- Pull latest system updates
- Review agent performance
- Update templates if needed

## Related Documentation

- [Developer Setup](./dev-setup.md) - Installation guide
- [Testing](./testing.md) - Testing procedures
- [Security](./security.md) - Security considerations
- [Bootstrap Guide](./bootstrap-guide.md) - Project initialization