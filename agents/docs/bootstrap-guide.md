# Bootstrap Guide

## Overview

The `/bootstrap` command is a powerful global slash command that analyzes any repository and sets up comprehensive Claude Code configuration, including documentation consolidation and optional Claude assets (CLAUDE.md, agents, hooks).

## Command Usage

### Basic Syntax
```text
/bootstrap [flags] [notes]
```

### Available Flags

| Flag | Description |
|------|-------------|
| `--docs-only` | Only create/update documentation, no Claude assets |
| `--bootstrap-only` | Skip docs, only set up CLAUDE.md, agents, hooks |
| `--agents` | Include `.claude/agents/*` configurations |
| `--hooks` | Include `.claude/settings.json` with safe hooks |
| `--yes` | Auto-approve changes (skip confirmation prompt) |

### Usage Examples

#### 1. Full Bootstrap (Recommended for New Projects)
```text
/bootstrap --agents --hooks
```
This will:
- Analyze your repository structure
- Create comprehensive documentation in `/docs/`
- Set up CLAUDE.md with project-specific instructions
- Install agent configurations in `.claude/agents/`
- Configure safe, non-destructive hooks

#### 2. Documentation Only
```text
/bootstrap --docs-only
```
Perfect for:
- Existing projects with Claude setup
- Documentation refresh/consolidation
- Non-invasive repository analysis

#### 3. Quick Setup (Claude Assets Only)
```text
/bootstrap --bootstrap-only --agents
```
Ideal when:
- Documentation already exists
- You want quick Claude Code configuration
- Focus on agent setup without docs

#### 4. Automated Setup
```text
/bootstrap --yes --agents --hooks
```
For CI/CD or when you trust the system completely.

## What Bootstrap Does

### Phase 1: Exploration
The bootstrap agent performs a comprehensive repository scan:
- Detects programming languages and frameworks
- Identifies package managers and build tools
- Locates configuration files
- Maps project structure
- Finds existing documentation

### Phase 2: Planning
Creates an action plan showing:
- Which documentation to create/update
- Existing docs to consolidate or archive
- Claude assets to generate
- Files that will be modified

### Phase 3: Execution (with approval)
Upon approval (or with `--yes` flag):
- Creates/updates documentation in `/docs/`
- Generates CLAUDE.md from templates
- Sets up agent configurations if requested
- Installs hooks if specified
- Archives outdated documentation

### Phase 4: Summary
Provides a comprehensive report:
- Created/updated files checklist
- Archived documentation locations
- Key commands to run the project
- Next steps and TODOs

## Template System

### Template Location
Templates are stored in `~/.claude/templates/bootstrap/`:
```
templates/bootstrap/
├── CLAUDE.md              # Main project instructions
├── agents/                # Agent configurations
│   ├── foundation.md      # Core setup and principles
│   ├── operations-and-safety.md
│   ├── stack-preferences.md
│   ├── style-and-conventions.md
│   └── testing-and-quality.md
└── hooks/                 # Hook scripts
    ├── auto-format.sh     # Automatic code formatting
    └── guard-unsafe.sh    # Safety checks
```

### Customizing Templates

#### Global Customization
Edit templates in `~/.claude/templates/bootstrap/` to affect all future projects:
```bash
# Edit the main template
vim ~/.claude/templates/bootstrap/CLAUDE.md

# Customize agent configs
vim ~/.claude/templates/bootstrap/agents/stack-preferences.md
```

#### Project-Specific Overrides
After bootstrap, customize `.claude/` files in your project:
```bash
# Project-specific instructions
vim .claude/CLAUDE.md

# Custom agent configurations
vim .claude/agents/custom-agent.md
```

## Generated Documentation

Bootstrap creates/updates the following in `/docs/`:

### Standard Documentation Set
1. **overview.md** - Project purpose and user journeys
2. **architecture.md** - System design and module structure
3. **api.md** - API endpoints and integrations
4. **data-model.md** - Database schema and relationships
5. **dev-setup.md** - Development environment setup
6. **testing.md** - Testing procedures and coverage
7. **security.md** - Security considerations
8. **code-map.md** - Directory structure with descriptions
9. **decisions/0001-architecture-baseline.md** - Architecture Decision Record

### Bootstrap-Specific Additions
- Links between all documentation files
- Mermaid diagrams for system visualization
- Command references and examples
- Environment variable documentation (redacted)

## Hook System

### Available Hooks
When using `--hooks`, bootstrap installs:

#### auto-format.sh
Automatically formats code before operations:
- Runs Prettier for JavaScript/TypeScript
- Applies Black for Python
- Uses gofmt for Go
- Configurable per project

#### guard-unsafe.sh
Prevents potentially dangerous operations:
- Blocks force pushes to main/master
- Prevents secret commits
- Validates branch naming
- Checks for large files

### Hook Configuration
Hooks are configured in `.claude/settings.json`:
```json
{
  "hooks": {
    "pre-commit": ".claude/hooks/auto-format.sh",
    "pre-push": ".claude/hooks/guard-unsafe.sh"
  }
}
```

## Best Practices

### For New Projects
1. Run `/bootstrap --agents --hooks` immediately after project creation
2. Review generated CLAUDE.md and customize as needed
3. Commit the `.claude/` directory to version control
4. Share with team members using Claude Code

### For Existing Projects
1. Start with `/bootstrap --docs-only` to assess current state
2. Review the consolidation plan before proceeding
3. Back up existing documentation if concerned
4. Run full bootstrap after review

### For Team Projects
1. Run bootstrap on a feature branch first
2. Review changes with team
3. Customize templates for team standards
4. Document team-specific conventions in CLAUDE.md

## Troubleshooting

### Common Issues

#### "No agents found after bootstrap"
- Ensure installation completed: `./install.sh`
- Check agent files exist: `ls ~/.claude/agents/`
- Restart Claude Code

#### "Bootstrap command not recognized"
- Verify global commands installed: `ls ~/.claude/commands/`
- Re-run installation script
- Check Claude Code version compatibility

#### "Documentation not generating"
- Ensure write permissions in project directory
- Check for `.gitignore` blocking `/docs/`
- Run with `--yes` flag to skip confirmation

#### "Hooks not executing"
- Verify hook scripts are executable: `chmod +x .claude/hooks/*.sh`
- Check `.claude/settings.json` configuration
- Test hooks manually: `bash .claude/hooks/auto-format.sh`

### Debug Mode
For detailed output during bootstrap:
```text
/bootstrap --docs-only  # Start with read-only mode
# Review the plan carefully
/bootstrap --yes  # Then proceed if satisfied
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Bootstrap Documentation
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'

jobs:
  bootstrap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Claude Code System
        run: |
          git clone https://github.com/[your-username]/claude-code-agent-system.git
          cd claude-code-agent-system
          ./install.sh
      - name: Run Bootstrap
        run: |
          # Use Claude Code CLI when available
          # For now, document the manual step
          echo "Run '/bootstrap --docs-only' in Claude Code"
```

## Advanced Usage

### Conditional Bootstrap
Use notes to specify requirements:
```text
/bootstrap --agents "Focus on React and TypeScript setup"
```

### Multi-Repository Setup
Create a bootstrap script for multiple repos:
```bash
#!/bin/bash
for repo in repo1 repo2 repo3; do
  cd /path/to/$repo
  echo "Bootstrapping $repo..."
  # Run bootstrap via Claude Code
done
```

### Template Variables
Templates support variable substitution:
- `{{PROJECT_NAME}}` - Detected project name
- `{{FRAMEWORK}}` - Detected primary framework
- `{{LANGUAGE}}` - Primary programming language
- `{{TIMESTAMP}}` - Bootstrap timestamp

## Next Steps

After successful bootstrap:
1. Review generated documentation in `/docs/`
2. Customize CLAUDE.md for project-specific needs
3. Test agent coordination with a multi-step task
4. Configure additional MCP servers if needed
5. Set up team conventions and standards
6. Document domain-specific patterns

## Related Documentation

- [Architecture](./architecture.md) - System design details
- [Agent Reference](./agent-reference.md) - Complete agent capabilities
- [Developer Setup](./dev-setup.md) - Installation and configuration
- [Troubleshooting](./troubleshooting.md) - Common issues and solutions