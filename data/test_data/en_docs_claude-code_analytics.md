---
url: https://docs.anthropic.com/en/docs/claude-code/analytics
scraped_at: 2025-08-22T07:44:12.675345
title: Analytics - Anthropic
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
Administration
Analytics
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


Administration
# Analytics
Copy page
View detailed usage insights and productivity metrics for your organization’s Claude Code deployment.
Claude Code provides an analytics dashboard that helps organizations understand developer usage patterns, track productivity metrics, and optimize their Claude Code adoption.
Analytics are currently available only for organizations using Claude Code with the Anthropic API through the Anthropic Console.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#access-analytics)
Access analytics
Navigate to the analytics dashboard at [console.anthropic.com/claude_code](https://console.anthropic.com/claude_code).
### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#required-roles)
Required roles
  * **Primary Owner**
  * **Owner**
  * **Billing**
  * **Admin**
  * **Developer**


Users with **User** , **Claude Code User** or **Membership Admin** roles cannot access analytics.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#available-metrics)
Available metrics
### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#lines-of-code-accepted)
Lines of code accepted
Total lines of code written by Claude Code that users have accepted in their sessions.
  * Excludes rejected code suggestions
  * Doesn’t track subsequent deletions


### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#suggestion-accept-rate)
Suggestion accept rate
Percentage of times users accept code editing tool usage, including:
  * Edit
  * MultiEdit
  * Write
  * NotebookEdit


### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#activity)
Activity
**users** : Number of active users in a given day (number on left Y-axis)
**sessions** : Number of active sessions in a given day (number on right Y-axis)
### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#spend)
Spend
**users** : Number of active users in a given day (number on left Y-axis)
**spend** : Total dollars spent in a given day (number on right Y-axis)
### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#team-insights)
Team insights
**Members** : All users who have authenticated to Claude Code
  * API key users are displayed by **API key identifier**
  * OAuth users are displayed by **email address**


**Spend this month:** Per-user total spend for the current month.
**Lines this month:** Per-user total of accepted code lines for the current month.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#using-analytics-effectively)
Using analytics effectively
### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#monitor-adoption)
Monitor adoption
Track team member status to identify:
  * Active users who can share best practices
  * Overall adoption trends across your organization


### 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#measure-productivity)
Measure productivity
Tool acceptance rates and code metrics help you:
  * Understand developer satisfaction with Claude Code suggestions
  * Track code generation effectiveness
  * Identify opportunities for training or process improvements


## 
[​](https://docs.anthropic.com/en/docs/claude-code/analytics#related-resources)
Related resources
  * [Monitoring usage with OpenTelemetry](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) for custom metrics and alerting
  * [Identity and access management](https://docs.anthropic.com/en/docs/claude-code/iam) for role configuration


Was this page helpful?
YesNo
[Costs](https://docs.anthropic.com/en/docs/claude-code/costs)[Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
On this page
  * [Access analytics](https://docs.anthropic.com/en/docs/claude-code/analytics#access-analytics)
  * [Required roles](https://docs.anthropic.com/en/docs/claude-code/analytics#required-roles)
  * [Available metrics](https://docs.anthropic.com/en/docs/claude-code/analytics#available-metrics)
  * [Lines of code accepted](https://docs.anthropic.com/en/docs/claude-code/analytics#lines-of-code-accepted)
  * [Suggestion accept rate](https://docs.anthropic.com/en/docs/claude-code/analytics#suggestion-accept-rate)
  * [Activity](https://docs.anthropic.com/en/docs/claude-code/analytics#activity)
  * [Spend](https://docs.anthropic.com/en/docs/claude-code/analytics#spend)
  * [Team insights](https://docs.anthropic.com/en/docs/claude-code/analytics#team-insights)
  * [Using analytics effectively](https://docs.anthropic.com/en/docs/claude-code/analytics#using-analytics-effectively)
  * [Monitor adoption](https://docs.anthropic.com/en/docs/claude-code/analytics#monitor-adoption)
  * [Measure productivity](https://docs.anthropic.com/en/docs/claude-code/analytics#measure-productivity)
  * [Related resources](https://docs.anthropic.com/en/docs/claude-code/analytics#related-resources)



