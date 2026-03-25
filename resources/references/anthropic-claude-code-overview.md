# Anthropic Claude Code Overview
Source: https://docs.anthropic.com/en/docs/claude-code/overview
Downloaded: 2026-03-25
Note: This is a local copy for reference. Check the source URL for the most current version.

---

## What is Claude Code?

Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. It is available in your terminal, IDE, desktop app, and browser.

Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done.

## Installation

### Terminal (Recommended)

**macOS, Linux, WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

Then start Claude Code in any project:
```bash
cd your-project
claude
```

You'll be prompted to log in on first use.

### Other Environments

- **VS Code / Cursor**: Search for "Claude Code" in the Extensions view
- **JetBrains**: Install the Claude Code plugin from the JetBrains Marketplace
- **Desktop App**: Available for macOS and Windows
- **Web**: Start coding at [claude.ai/code](https://claude.ai/code)

## What You Can Do

### Automate tedious tasks
Write tests, fix lint errors, resolve merge conflicts, update dependencies, and write release notes:
```bash
claude "write tests for the auth module, run them, and fix any failures"
```

### Build features and fix bugs
Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works. For bugs, paste an error message or describe the symptom.

### Create commits and pull requests
Claude Code works directly with git:
```bash
claude "commit my changes with a descriptive message"
```

### Connect your tools with MCP
The Model Context Protocol (MCP) is an open standard for connecting AI tools to external data sources. Claude Code can read design docs in Google Drive, update tickets in Jira, pull data from Slack, or use custom tooling.

### Customize with instructions, skills, and hooks
- **CLAUDE.md**: A markdown file in your project root that Claude Code reads at the start of every session. Use it for coding standards, architecture decisions, and preferred libraries.
- **Custom commands**: Package repeatable workflows your team can share (e.g., `/review-pr`, `/deploy-staging`)
- **Hooks**: Run shell commands before or after Claude Code actions

### Run agent teams and build custom agents
Spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates, assigns subtasks, and merges results.

### Pipe, script, and automate with the CLI
Claude Code is composable and follows the Unix philosophy:
```bash
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"
```

### Schedule recurring tasks
Run Claude on a schedule: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge.

## Use Claude Code Everywhere

Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them.

| I want to... | Best option |
|---|---|
| Continue a local session from my phone | Remote Control |
| Push events from Telegram, Discord, etc. | Channels |
| Start a task locally, continue on mobile | Web or Claude iOS app |
| Run Claude on a recurring schedule | Cloud or Desktop scheduled tasks |
| Automate PR reviews and issue triage | GitHub Actions or GitLab CI/CD |
| Get automatic code review on every PR | GitHub Code Review |
| Route bug reports from Slack to PRs | Slack integration |
| Debug live web applications | Chrome extension |
| Build custom agents | Agent SDK |

## Next Steps

- [Quickstart](https://code.claude.com/docs/en/quickstart) -- Walk through your first real task
- [Store instructions and memories](https://code.claude.com/docs/en/memory) -- Give Claude persistent instructions with CLAUDE.md
- [Common workflows](https://code.claude.com/docs/en/common-workflows) -- Patterns for getting the most out of Claude Code
- [Settings](https://code.claude.com/docs/en/settings) -- Customize Claude Code for your workflow
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) -- Solutions for common issues
