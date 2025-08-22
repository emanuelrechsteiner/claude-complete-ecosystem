## Testing

How to test locally:
- Verify agents list inside Claude Code with `/agents`.
- Exercise research flow after MCP setup with a prompt like: "Research React 19 features".
- Test bootstrap command with `/bootstrap --docs-only` for non-destructive verification.

Quality checks:
- Shell scripts: run `shellcheck install.sh setup-firecrawl-mcp.sh uninstall.sh`.
- Markdown: run a Markdown linter (e.g., `markdownlint`) on `*.md`.
- Bootstrap templates: verify template syntax and variable substitution.

Coverage and gaps:
- No code unit tests; focus on manual verification of agent activation, ledger updates, and observation capture.

Bootstrap Feature Testing:
1. **Dry Run Test**: `/bootstrap --docs-only` (read-only exploration)
2. **Template Test**: Verify templates in `templates/bootstrap/` are valid
3. **Hook Test**: Check hook scripts execute safely with `bash -n templates/bootstrap/hooks/*.sh`
4. **Integration Test**: Create test project and run `/bootstrap --agents --hooks`

Agent Coordination Tests:
- Multi-agent workflow: "Build a todo app" should trigger control → planning → research → implementation agents
- Sequential handoffs: Verify agents report to control-agent before/during/after work
- Parallel execution: Research and planning agents should run concurrently when appropriate

Ledger Verification:
- Check JSON validity: `jq . ledgers/*.json`
- Verify task state transitions: pending → in_progress → completed
- Confirm dependency tracking between agents

Next smoke tests:
- Ensure control-agent delegates on multi-step prompts.
- Confirm observation artifacts update when ledgers change.
- Validate Firecrawl calls succeed when key is present.
- Test bootstrap command creates proper CLAUDE.md and agent configs.
- Verify hooks execute without errors.


