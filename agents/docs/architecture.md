## Architecture

Structure:
- Monorepo-style documentation project. No build runtime. Source-of-truth is Markdown/JSON + shell scripts.

Modules and responsibilities:
- `agents/`: Role definitions and protocols per agent; consumed by Claude Code.
  - Includes `project-bootstrap-agent.md` for project initialization
- `observation/`: Hook specifications and summaries for passive event capture.
- `ledgers/`: Task ledgers per agent in JSON; single-source-of-truth for progress.
- `global-observation/`: Cross-project ledger persisted between sessions/devices.
- `templates/`: Project bootstrap templates and configurations
  - `bootstrap/`: CLAUDE.md and agent templates for new projects
  - `commands/`: Global slash command definitions including `/bootstrap`
  - `hooks/`: Safe, non-destructive hook scripts (auto-format, guard-unsafe)
- Root scripts: `install.sh`, `setup-firecrawl-mcp.sh`, `uninstall.sh` for system lifecycle.
- Root specs: `CLAUDE.md`, `agent-protocols.md`, `memory.md` define the mandatory workflow and memory import.

Dependency hotspots:
- Control-agent is gateway for multi-agent work; all multi-step flows pass through it.
- Research-agent depends on Firecrawl MCP when available.
- Observation depends on ledger updates and hooks to ensure >99% capture.
- Bootstrap system depends on templates directory for project initialization.

Extension points:
- Add new agents by adding files in `~/.claude/agents/` (see `docs/dev-setup.md`).
- Add new MCP servers by extending `.env` and the setup script.
- Customize bootstrap templates in `templates/bootstrap/` for project-specific needs.
- Add new global commands in `templates/commands/` for Claude Code.

Package mini-profiles (logical, not NPM/PyPi):
- Agents: YAML frontmatter + narrative instructions
- Ledgers: JSON finite-state lifecycle for tasks
- Observation: Markdown specs + JSON streams


