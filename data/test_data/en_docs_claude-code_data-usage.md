---
url: https://docs.anthropic.com/en/docs/claude-code/data-usage
scraped_at: 2025-08-22T08:59:42.996784
title: Data usage - Anthropic
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
Data usage
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
# Data usage
Copy page
Learn about Anthropic’s data usage policies for Claude
## 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-policies)
Data policies
### 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-training-policy)
Data training policy
By default, Anthropic does not train generative models using code or prompts that are sent to Claude Code.
We aim to be fully transparent about how we use your data. We may use feedback to improve our products and services, but we will not train generative models using your feedback from Claude Code.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#development-partner-program)
Development Partner Program
If you explicitly opt in to methods to provide us with materials to train on, such as via the [Development Partner Program](https://support.anthropic.com/en/articles/11174108-about-the-development-partner-program), we may use those materials provided to train our models. An organization admin can expressly opt-in to the Development Partner Program for their organization. Note that this program is available only for Anthropic first-party API, and not for Bedrock or Vertex users.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#feedback-transcripts)
Feedback transcripts
If you choose to send us feedback about Claude Code, such as transcripts of your usage, Anthropic may use that feedback to debug related issues and improve Claude Code’s functionality (e.g., to reduce the risk of similar bugs occurring in the future). We will not train generative models using this feedback. Given their potentially sensitive nature, we store user feedback transcripts for only 30 days.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-retention)
Data retention
You can use an API key from a zero data retention organization. When doing so, Claude Code will not retain your chat transcripts on our servers. Users’ local Claude Code clients may store sessions locally for up to 30 days so that users can resume them. This behavior is configurable.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#privacy-safeguards)
Privacy safeguards
We have implemented several safeguards to protect your data, including:
  * Limited retention periods for sensitive information
  * Restricted access to user session data
  * Clear policies against using feedback for model training


For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).
## 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-flow-and-dependencies)
Data flow and dependencies
![Claude Code data flow diagram](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/images/claude-code-data-flow.png)
Claude Code is installed from [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code runs locally. In order to interact with the LLM, Claude Code sends data over the network. This data includes all user prompts and model outputs. The data is encrypted in transit via TLS and is not encrypted at rest. Claude Code is compatible with most popular VPNs and LLM proxies.
Claude Code is built on Anthropic’s APIs. For details regarding our API’s security controls, including our API logging procedures, please refer to compliance artifacts offered in the [Anthropic Trust Center](https://trust.anthropic.com).
## 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#telemetry-services)
Telemetry services
Claude Code connects from users’ machines to the Statsig service to log operational metrics such as latency, reliability, and usage patterns. This logging does not include any code or file paths. Data is encrypted in transit using TLS and at rest using 256-bit AES encryption. Read more in the [Statsig security documentation](https://www.statsig.com/trust/security). To opt out of Statsig telemetry, set the `DISABLE_TELEMETRY` environment variable.
Claude Code connects from users’ machines to Sentry for operational error logging. The data is encrypted in transit using TLS and at rest using 256-bit AES encryption. Read more in the [Sentry security documentation](https://sentry.io/security/). To opt out of error logging, set the `DISABLE_ERROR_REPORTING` environment variable.
When users run the `/bug` command, a copy of their full conversation history including code is sent to Anthropic. The data is encrypted in transit and at rest. Optionally, a Github issue is created in our public repository. To opt out of bug reporting, set the `DISABLE_BUG_COMMAND` environment variable.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/data-usage#default-behaviors-by-api-provider)
Default behaviors by API provider
By default, we disable all non-essential traffic (including error reporting, telemetry, and bug reporting functionality) when using Bedrock or Vertex. You can also opt out of all of these at once by setting the `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` environment variable. Here are the full default behaviors:
Service| Anthropic API| Vertex API| Bedrock API  
---|---|---|---  
**Statsig (Metrics)**|  Default on.`DISABLE_TELEMETRY=1` to disable.| Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.| Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.  
**Sentry (Errors)**|  Default on.`DISABLE_ERROR_REPORTING=1` to disable.| Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.| Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.  
**Anthropic API (`/bug` reports)**| Default on.`DISABLE_BUG_COMMAND=1` to disable.| Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.| Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.  
All environment variables can be checked into `settings.json` ([read more](https://docs.anthropic.com/en/docs/claude-code/settings)).
Was this page helpful?
YesNo
[Security](https://docs.anthropic.com/en/docs/claude-code/security)[Monitoring](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage)
[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
On this page
  * [Data policies](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-policies)
  * [Data training policy](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-training-policy)
  * [Development Partner Program](https://docs.anthropic.com/en/docs/claude-code/data-usage#development-partner-program)
  * [Feedback transcripts](https://docs.anthropic.com/en/docs/claude-code/data-usage#feedback-transcripts)
  * [Data retention](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-retention)
  * [Privacy safeguards](https://docs.anthropic.com/en/docs/claude-code/data-usage#privacy-safeguards)
  * [Data flow and dependencies](https://docs.anthropic.com/en/docs/claude-code/data-usage#data-flow-and-dependencies)
  * [Telemetry services](https://docs.anthropic.com/en/docs/claude-code/data-usage#telemetry-services)
  * [Default behaviors by API provider](https://docs.anthropic.com/en/docs/claude-code/data-usage#default-behaviors-by-api-provider)


![Claude Code data flow diagram](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/images/claude-code-data-flow.png)

