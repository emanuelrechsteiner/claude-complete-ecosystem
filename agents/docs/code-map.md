## Code Map

Top-level tree (depth ~2) and blurbs:

- `agents/` — Agent definitions and capabilities
  - `planning-agent.md` — Planning and orchestration
  - `control-agent.md` — Quality gates and delegation
  - `research-agent.md` — Firecrawl-enabled research
  - `ui-agent.md`, `ux-agent.md`, `backend-agent.md`, `documentation-agent.md`, `version-control-agent.md` — Specializations

- `observation/` — Hooks, summaries, and safety protocols
  - `agent-hooks.md` — Passive capture contract
  - `safe-update-protocol.md` — Safety and rollback

- `ledgers/` — JSON task ledgers per agent

- `global-observation/` — Cross-project observation ledger

- Root specs and scripts
  - `CLAUDE.md` — Mandatory global workflow
  - `agent-protocols.md` — Communication protocols
  - `memory.md` — Auto-import memory hook
  - `install.sh`, `uninstall.sh`, `setup-firecrawl-mcp.sh` — Lifecycle scripts
  - `example.env` — Env template

See `docs/architecture.md` for relationships and `docs/dev-setup.md` for commands.


