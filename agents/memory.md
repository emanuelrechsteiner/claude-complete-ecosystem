# User Memory - Mandatory Global Workflow

**AUTOMATIC IMPORT**: Global agentic workflow is mandatory for all sessions.

Import global workflow: @~/.claude/CLAUDE.md

## Automatic Enforcement Rules

### Always Active - No User Request Required
- **Control-agent coordination**: Automatically activated for multi-step tasks
- **Agent delegation**: Control-agent MUST delegate, never execute directly
- **Workflow compliance**: Applied regardless of user prompt content
- **Global consistency**: Same workflow across all projects and sessions

### Agent Activation Patterns
These patterns activate automatically when relevant tasks are detected:

#### Trigger Patterns (Auto-Detected)
- **Build/create/develop mentions** → Activates control-agent + planning-agent + research-agent (parallel)
- **Technical research needed** → Activates research-agent immediately
- **New technologies/APIs mentioned** → Activates research-agent for documentation
- **Backend/API work** → Activates backend-agent (after research provides documentation)
- **Frontend/React/UI work** → Activates frontend-agent (after research provides documentation)
- **Testing requirements** → Activates testing-agent
- **Documentation needs** → Activates documentation-agent
- **Git/version control** → Activates version-control-agent

### Critical Reminders
- **User doesn't need to request agentic workflow** - it's automatic
- **Control-agent always delegates** - never executes tasks directly
- **All agents report to control-agent** - mandatory coordination
- **60-minute commit frequency** - enforced for all agents

This memory ensures the global agentic workflow is active in every Claude Code session, regardless of project or user prompt content.