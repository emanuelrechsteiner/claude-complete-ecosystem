## Security

Secrets handling:
- Do not commit `.env`. Use `example.env` as a template.
- Redact keys in docs and issues (e.g., `fc-****`).

Auth/permissions:
- Research Agent uses Firecrawl MCP with `firecrawl-api-key` if configured.

Risks and quick wins:
- Risk: Accidental key commits → Ensure `.env` is gitignored (already configured).
- Risk: Over-permissive scripts → Review shell scripts and run `shellcheck`.


