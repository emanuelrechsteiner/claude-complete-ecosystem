---
url: https://docs.anthropic.com/en/docs/claude-code/interactive-mode
scraped_at: 2025-08-22T07:44:21.143682
title: Interactive mode - Anthropic
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)
English
Search...
⌘K
  * [Research](https://www.anthropic.com/research)
  * [Login](https://console.anthropic.com/login)
  * [Support](https://support.anthropic.com/)
  * [Discord](https://www.anthropic.com/discord)
  * [Sign up](https://console.anthropic.com/login)
  * [Sign up](https://console.anthropic.com/login)


Search...
Navigation
Reference
Interactive mode
[Welcome](https://docs.anthropic.com/en/home)[Developer Platform](https://docs.anthropic.com/en/docs/intro)[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)[Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp)[API Reference](https://docs.anthropic.com/en/api/messages)[Resources](https://docs.anthropic.com/en/resources/overview)[Release Notes](https://docs.anthropic.com/en/release-notes/overview)
##### Getting started
  * [Overview](https://docs.anthropic.com/en/docs/claude-code/overview)
  * [Quickstart](https://docs.anthropic.com/en/docs/claude-code/quickstart)
  * [Common workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows)


##### Build with Claude Code
  * [Claude Code SDK](https://docs.anthropic.com/en/docs/claude-code/sdk)
  * [Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
  * [Output styles](https://docs.anthropic.com/en/docs/claude-code/output-styles)
  * [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)
  * [GitHub Actions](https://docs.anthropic.com/en/docs/claude-code/github-actions)
  * [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/claude-code/mcp)
  * [Troubleshooting](https://docs.anthropic.com/en/docs/claude-code/troubleshooting)


##### Deployment
  * [Overview](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations)
  * [Amazon Bedrock](https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock)
  * [Google Vertex AI](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai)
  * [Corporate proxy](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy)
  * [LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
  * [Development containers](https://docs.anthropic.com/en/docs/claude-code/devcontainer)


##### Administration
  * [Advanced installation](https://docs.anthropic.com/en/docs/claude-code/setup)
  * [Identity and Access Management](https://docs.anthropic.com/en/docs/claude-code/iam)
  * [Security](https://docs.anthropic.com/en/docs/claude-code/security)
  * [Data usage](https://docs.anthropic.com/en/docs/claude-code/data-usage)
  * [Monitoring](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage)
  * [Costs](https://docs.anthropic.com/en/docs/claude-code/costs)
  * [Analytics](https://docs.anthropic.com/en/docs/claude-code/analytics)


##### Configuration
  * [Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
  * [Add Claude Code to your IDE](https://docs.anthropic.com/en/docs/claude-code/ide-integrations)
  * [Terminal configuration](https://docs.anthropic.com/en/docs/claude-code/terminal-config)
  * [Memory management](https://docs.anthropic.com/en/docs/claude-code/memory)
  * [Status line configuration](https://docs.anthropic.com/en/docs/claude-code/statusline)


##### Reference
  * [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
  * [Interactive mode](https://docs.anthropic.com/en/docs/claude-code/interactive-mode)
  * [Slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
  * [Hooks reference](https://docs.anthropic.com/en/docs/claude-code/hooks)


##### Resources
  * [Legal and compliance](https://docs.anthropic.com/en/docs/claude-code/legal-and-compliance)


Reference
# Interactive mode
Copy page
Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#keyboard-shortcuts)
Keyboard shortcuts
### 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#general-controls)
General controls
Shortcut| Description| Context  
---|---|---  
`Ctrl+C`| Cancel current input or generation| Standard interrupt  
`Ctrl+D`| Exit Claude Code session| EOF signal  
`Ctrl+L`| Clear terminal screen| Keeps conversation history  
`Up/Down arrows`| Navigate command history| Recall previous inputs  
`Esc` + `Esc`| Edit previous message| Double-escape to modify  
### 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#multiline-input)
Multiline input
Method| Shortcut| Context  
---|---|---  
Quick escape| `\` + `Enter`| Works in all terminals  
macOS default| `Option+Enter`| Default on macOS  
Terminal setup| `Shift+Enter`| After `/terminal-setup`  
Control sequence| `Ctrl+J`| Line feed character for multiline  
Paste mode| Paste directly| For code blocks, logs  
### 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#quick-commands)
Quick commands
Shortcut| Description| Notes  
---|---|---  
`#` at start| Memory shortcut - add to CLAUDE.md| Prompts for file selection  
`/` at start| Slash command| See [slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)  
## 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#vim-mode)
Vim mode
Enable vim-style editing with `/vim` command or configure permanently via `/config`.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#mode-switching)
Mode switching
Command| Action| From mode  
---|---|---  
`Esc`| Enter NORMAL mode| INSERT  
`i`| Insert before cursor| NORMAL  
`I`| Insert at beginning of line| NORMAL  
`a`| Insert after cursor| NORMAL  
`A`| Insert at end of line| NORMAL  
`o`| Open line below| NORMAL  
`O`| Open line above| NORMAL  
### 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#navigation-normal-mode)
Navigation (NORMAL mode)
Command| Action  
---|---  
`h`/`j`/`k`/`l`| Move left/down/up/right  
`w`| Next word  
`e`| End of word  
`b`| Previous word  
`0`| Beginning of line  
`$`| End of line  
`^`| First non-blank character  
`gg`| Beginning of input  
`G`| End of input  
### 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#editing-normal-mode)
Editing (NORMAL mode)
Command| Action  
---|---  
`x`| Delete character  
`dd`| Delete line  
`D`| Delete to end of line  
`dw`/`de`/`db`| Delete word/to end/back  
`cc`| Change line  
`C`| Change to end of line  
`cw`/`ce`/`cb`| Change word/to end/back  
`.`| Repeat last change  
Configure your preferred line break behavior in terminal settings. Run `/terminal-setup` to install Shift+Enter binding for iTerm2 and VS Code terminals.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#command-history)
Command history
Claude Code maintains command history for the current session:
  * History is stored per working directory
  * Cleared with `/clear` command
  * Use Up/Down arrows to navigate (see keyboard shortcuts above)
  * **Ctrl+R** : Reverse search through history (if supported by terminal)
  * **Note** : History expansion (`!`) is disabled by default


## 
[​](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#see-also)
See also
  * [Slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) - Interactive session commands
  * [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference) - Command-line flags and options
  * [Settings](https://docs.anthropic.com/en/docs/claude-code/settings) - Configuration options
  * [Memory management](https://docs.anthropic.com/en/docs/claude-code/memory) - Managing CLAUDE.md files


Was this page helpful?
YesNo
[CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)[Slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
On this page
  * [Keyboard shortcuts](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#keyboard-shortcuts)
  * [General controls](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#general-controls)
  * [Multiline input](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#multiline-input)
  * [Quick commands](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#quick-commands)
  * [Vim mode](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#vim-mode)
  * [Mode switching](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#mode-switching)
  * [Navigation (NORMAL mode)](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#navigation-normal-mode)
  * [Editing (NORMAL mode)](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#editing-normal-mode)
  * [Command history](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#command-history)
  * [See also](https://docs.anthropic.com/en/docs/claude-code/interactive-mode#see-also)



