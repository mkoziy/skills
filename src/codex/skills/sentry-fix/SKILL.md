---
name: sentry-fix
description: Find and fix issues from Sentry using the Sentry MCP server. Use when asked to fix Sentry errors, debug production issues, investigate exceptions, or resolve bugs reported in Sentry. Analyzes stack traces, breadcrumbs, traces, and context to identify root causes.
allowed-tools: Bash, Read, Glob, Grep
---

# Fix Sentry Issues

Discover, analyze, and fix production issues using Sentry's MCP server.

## Phase 0: Verify MCP Connection

Call `find_projects` with no filters. If the call fails or the Sentry MCP server is not available, stop and tell the user:

```
The Sentry MCP server is not connected. Add it to your Codex config:

  Open (or create) ~/.codex/config.yaml and add:

    mcpServers:
      sentry:
        type: http
        url: https://mcp.sentry.dev/mcp

Then restart Codex and try again.
```

If `find_projects` succeeds, note the list of available organizations and projects — you will use it in Phase 1.

{{ include "common/skills/sentry-fix/_body.md" }}
