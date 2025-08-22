---
url: https://docs.anthropic.com/en/docs/claude-code/third-party-integrations
scraped_at: 2025-08-22T08:59:12.157163
title: Enterprise deployment overview - Anthropic
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
Deployment
Enterprise deployment overview
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


Deployment
# Enterprise deployment overview
Copy page
Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements.
This page provides an overview of available deployment options and helps you choose the right configuration for your organization.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#provider-comparison)
Provider comparison
Feature| Anthropic| Amazon Bedrock| Google Vertex AI  
---|---|---|---  
Regions| Supported [countries](https://www.anthropic.com/supported-countries)| Multiple AWS [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)| Multiple GCP [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)  
Prompt caching| Enabled by default| Enabled by default| Enabled by default  
Authentication| API key| AWS credentials (IAM)| GCP credentials (OAuth/Service Account)  
Cost tracking| Dashboard| AWS Cost Explorer| GCP Billing  
Enterprise features| Teams, usage monitoring| IAM policies, CloudTrail| IAM roles, Cloud Audit Logs  
## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#cloud-providers)
Cloud providers
## [Amazon BedrockUse Claude models through AWS infrastructure with IAM-based authentication and AWS-native monitoring](https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock)## [Google Vertex AIAccess Claude models via Google Cloud Platform with enterprise-grade security and compliance](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai)
## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#corporate-infrastructure)
Corporate infrastructure
## [Corporate ProxyConfigure Claude Code to work with your organization’s proxy servers and SSL/TLS requirements](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy)## [LLM GatewayDeploy centralized model access with usage tracking, budgeting, and audit logging](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#configuration-overview)
Configuration overview
Claude Code supports flexible configuration options that allow you to combine different providers and infrastructure:
Understand the difference between:
  * **Corporate proxy** : An HTTP/HTTPS proxy for routing traffic (set via `HTTPS_PROXY` or `HTTP_PROXY`)
  * **LLM Gateway** : A service that handles authentication and provides provider-compatible endpoints (set via `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, or `ANTHROPIC_VERTEX_BASE_URL`)


Both configurations can be used in tandem.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-bedrock-with-corporate-proxy)
Using Bedrock with corporate proxy
Route Bedrock traffic through a corporate HTTP/HTTPS proxy:
Copy
```
# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
# Configure corporate proxy
export HTTPS_PROXY='https://proxy.example.com:8080'

```

### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-bedrock-with-llm-gateway)
Using Bedrock with LLM Gateway
Use a gateway service that provides Bedrock-compatible endpoints:
Copy
```
# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
# Configure LLM gateway
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1 # If gateway handles AWS auth

```

### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-vertex-ai-with-corporate-proxy)
Using Vertex AI with corporate proxy
Route Vertex AI traffic through a corporate HTTP/HTTPS proxy:
Copy
```
# Enable Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id
# Configure corporate proxy
export HTTPS_PROXY='https://proxy.example.com:8080'

```

### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-vertex-ai-with-llm-gateway)
Using Vertex AI with LLM Gateway
Combine Google Vertex AI models with an LLM gateway for centralized management:
Copy
```
# Enable Vertex
export CLAUDE_CODE_USE_VERTEX=1
# Configure LLM gateway
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1 # If gateway handles GCP auth

```

### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#authentication-configuration)
Authentication configuration
Claude Code uses the `ANTHROPIC_AUTH_TOKEN` for the `Authorization` header when needed. The `SKIP_AUTH` flags (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) are used in LLM gateway scenarios where the gateway handles provider authentication.
## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#choosing-the-right-deployment-configuration)
Choosing the right deployment configuration
Consider these factors when selecting your deployment approach:
### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#direct-provider-access)
Direct provider access
Best for organizations that:
  * Want the simplest setup
  * Have existing AWS or GCP infrastructure
  * Need provider-native monitoring and compliance


### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#corporate-proxy)
Corporate proxy
Best for organizations that:
  * Have existing corporate proxy requirements
  * Need traffic monitoring and compliance
  * Must route all traffic through specific network paths


### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#llm-gateway)
LLM Gateway
Best for organizations that:
  * Need usage tracking across teams
  * Want to dynamically switch between models
  * Require custom rate limiting or budgets
  * Need centralized authentication management


## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#debugging)
Debugging
When debugging your deployment:
  * Use the `claude /status` [slash command](https://docs.anthropic.com/en/docs/claude-code/slash-commands). This command provides observability into any applied authentication, proxy, and URL settings.
  * Set environment variable `export ANTHROPIC_LOG=debug` to log requests.


## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#best-practices-for-organizations)
Best practices for organizations
### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#1-invest-in-documentation-and-memory)
1. Invest in documentation and memory
We strongly recommend investing in documentation so that Claude Code understands your codebase. Organizations can deploy CLAUDE.md files at multiple levels:
  * **Organization-wide** : Deploy to system directories like `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) for company-wide standards
  * **Repository-level** : Create `CLAUDE.md` files in repository roots containing project architecture, build commands, and contribution guidelines. Check these into source control so all users benefit
[Learn more](https://docs.anthropic.com/en/docs/claude-code/memory).


### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#2-simplify-deployment)
2. Simplify deployment
If you have a custom development environment, we find that creating a “one click” way to install Claude Code is key to growing adoption across an organization.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#3-start-with-guided-usage)
3. Start with guided usage
Encourage new users to try Claude Code for codebase Q&A, or on smaller bug fixes or feature requests. Ask Claude Code to make a plan. Check Claude’s suggestions and give feedback if it’s off-track. Over time, as users understand this new paradigm better, then they’ll be more effective at letting Claude Code run more agentically.
### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#4-configure-security-policies)
4. Configure security policies
Security teams can configure managed permissions for what Claude Code is and is not allowed to do, which cannot be overwritten by local configuration. [Learn more](https://docs.anthropic.com/en/docs/claude-code/security).
### 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#5-leverage-mcp-for-integrations)
5. Leverage MCP for integrations
MCP is a great way to give Claude Code more information, such as connecting to ticket management systems or error logs. We recommend that one central team configures MCP servers and checks a `.mcp.json` configuration into the codebase so that all users benefit. [Learn more](https://docs.anthropic.com/en/docs/claude-code/mcp).
At Anthropic, we trust Claude Code to power development across every Anthropic codebase. We hope you enjoy using Claude Code as much as we do!
## 
[​](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#next-steps)
Next steps
  * [Set up Amazon Bedrock](https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock) for AWS-native deployment
  * [Configure Google Vertex AI](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai) for GCP deployment
  * [Implement Corporate Proxy](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy) for network requirements
  * [Deploy LLM Gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway) for enterprise management
  * [Settings](https://docs.anthropic.com/en/docs/claude-code/settings) for configuration options and environment variables


Was this page helpful?
YesNo
[Troubleshooting](https://docs.anthropic.com/en/docs/claude-code/troubleshooting)[Amazon Bedrock](https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock)
[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
On this page
  * [Provider comparison](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#provider-comparison)
  * [Cloud providers](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#cloud-providers)
  * [Corporate infrastructure](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#corporate-infrastructure)
  * [Configuration overview](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#configuration-overview)
  * [Using Bedrock with corporate proxy](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-bedrock-with-corporate-proxy)
  * [Using Bedrock with LLM Gateway](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-bedrock-with-llm-gateway)
  * [Using Vertex AI with corporate proxy](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-vertex-ai-with-corporate-proxy)
  * [Using Vertex AI with LLM Gateway](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#using-vertex-ai-with-llm-gateway)
  * [Authentication configuration](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#authentication-configuration)
  * [Choosing the right deployment configuration](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#choosing-the-right-deployment-configuration)
  * [Direct provider access](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#direct-provider-access)
  * [Corporate proxy](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#corporate-proxy)
  * [LLM Gateway](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#llm-gateway)
  * [Debugging](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#debugging)
  * [Best practices for organizations](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#best-practices-for-organizations)
  * [1. Invest in documentation and memory](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#1-invest-in-documentation-and-memory)
  * [2. Simplify deployment](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#2-simplify-deployment)
  * [3. Start with guided usage](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#3-start-with-guided-usage)
  * [4. Configure security policies](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#4-configure-security-policies)
  * [5. Leverage MCP for integrations](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#5-leverage-mcp-for-integrations)
  * [Next steps](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations#next-steps)



