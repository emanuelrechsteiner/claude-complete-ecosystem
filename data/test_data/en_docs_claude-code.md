---
url: https://docs.anthropic.com/en/docs/claude-code
scraped_at: 2025-08-22T08:58:06.657952
title: Claude Code overview - Anthropic
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
Getting started
Claude Code overview
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


Getting started
# Claude Code overview
Copy page
Learn about Claude Code, Anthropic’s agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/overview#get-started-in-30-seconds)
Get started in 30 seconds
Prerequisites: [Node.js 18 or newer](https://nodejs.org/en/download/)
Copy
```
# Install Claude Code
npm install -g @anthropic-ai/claude-code
# Navigate to your project
cd your-awesome-project
# Start coding with Claude
claude

```

That’s it! You’re ready to start coding with Claude. [Continue with Quickstart (5 mins) →](https://docs.anthropic.com/en/docs/claude-code/quickstart)
(Got specific setup needs or hit issues? See [advanced setup](https://docs.anthropic.com/en/docs/claude-code/setup) or [troubleshooting](https://docs.anthropic.com/en/docs/claude-code/troubleshooting).)
## 
[​](https://docs.anthropic.com/en/docs/claude-code/overview#what-claude-code-does-for-you)
What Claude Code does for you
  * **Build features from descriptions** : Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
  * **Debug and fix issues** : Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
  * **Navigate any codebase** : Ask anything about your team’s codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with [MCP](https://docs.anthropic.com/en/docs/claude-code/mcp) can pull from external datasources like Google Drive, Figma, and Slack.
  * **Automate tedious tasks** : Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.


## 
[​](https://docs.anthropic.com/en/docs/claude-code/overview#why-developers-love-claude-code)
Why developers love Claude Code
  * **Works in your terminal** : Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.
  * **Takes action** : Claude Code can directly edit files, run commands, and create commits. Need more? [MCP](https://docs.anthropic.com/en/docs/claude-code/mcp) lets Claude read your design docs in Google Drive, update your tickets in Jira, or use _your_ custom developer tooling.
  * **Unix philosophy** : Claude Code is composable and scriptable. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` _works_. Your CI can run `claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"`.
  * **Enterprise-ready** : Use Anthropic’s API, or host on AWS or GCP. Enterprise-grade [security](https://docs.anthropic.com/en/docs/claude-code/security), [privacy](https://docs.anthropic.com/en/docs/claude-code/data-usage), and [compliance](https://trust.anthropic.com/) is built-in.


## 
[​](https://docs.anthropic.com/en/docs/claude-code/overview#next-steps)
Next steps
## [QuickstartSee Claude Code in action with practical examples](https://docs.anthropic.com/en/docs/claude-code/quickstart)## [Common workflowsStep-by-step guides for common workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows)## [TroubleshootingSolutions for common issues with Claude Code](https://docs.anthropic.com/en/docs/claude-code/troubleshooting)## [IDE setupAdd Claude Code to your IDE](https://docs.anthropic.com/en/docs/claude-code/ide-integrations)
## 
[​](https://docs.anthropic.com/en/docs/claude-code/overview#additional-resources)
Additional resources
## [Host on AWS or GCPConfigure Claude Code with Amazon Bedrock or Google Vertex AI](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations)## [SettingsCustomize Claude Code for your workflow](https://docs.anthropic.com/en/docs/claude-code/settings)## [CommandsLearn about CLI commands and controls](https://docs.anthropic.com/en/docs/claude-code/cli-reference)## [Reference implementationClone our development container reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer)## [SecurityDiscover Claude Code’s safeguards and best practices for safe usage](https://docs.anthropic.com/en/docs/claude-code/security)## [Privacy and data usageUnderstand how Claude Code handles your data](https://docs.anthropic.com/en/docs/claude-code/data-usage)
Was this page helpful?
YesNo
[Quickstart](https://docs.anthropic.com/en/docs/claude-code/quickstart)
[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
On this page
  * [Get started in 30 seconds](https://docs.anthropic.com/en/docs/claude-code/overview#get-started-in-30-seconds)
  * [What Claude Code does for you](https://docs.anthropic.com/en/docs/claude-code/overview#what-claude-code-does-for-you)
  * [Why developers love Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview#why-developers-love-claude-code)
  * [Next steps](https://docs.anthropic.com/en/docs/claude-code/overview#next-steps)
  * [Additional resources](https://docs.anthropic.com/en/docs/claude-code/overview#additional-resources)



