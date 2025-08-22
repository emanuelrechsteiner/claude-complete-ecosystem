---
title: Architecture Baseline and Trade-offs
status: accepted
date: 2025-08-10
---

Context:
- Documentation-first repository installing a global multi-agent workflow for Claude Code.
- No runtime services; file-based protocols and scripts.

Decision:
- Maintain agents, ledgers, and observation as Markdown/JSON artifacts with shell scripts for lifecycle.
- Centralize canonical docs under `docs/` and keep root README minimal as an entrypoint.

Consequences:
- Easy portability and auditability; minimal dependencies.
- No automated tests; rely on smoke tests and linters.

Open questions:
- Should we add CI for linting (`shellcheck`, `markdownlint`)?
- Formal schema for ledgers to enable validation?


