---
name: situ2001-plugin-setup
description: Install or refresh the situ2001 plugin for Codex and Claude Code from an existing local directory or marketplace.
---

# Situ2001 Plugin Setup

Follow the requested agent scope. When no agent is specified, consider both Codex and Claude Code and refresh existing installations for each.

## Select the workflow

Read only the reference for the agent and installation stage being handled:

- **Codex initial installation:** read [references/codex-initial-setup.md](references/codex-initial-setup.md) for source placement, marketplace creation, and installation.
- **Codex refresh after edits:** read [references/codex-refresh.md](references/codex-refresh.md) for cache version rotation and reinstallation.
- **Claude Code installation or refresh:** read [references/claude-setup-refresh.md](references/claude-setup-refresh.md) for live-directory loading or a persistent installation.

## Shared requirements

- Follow the target repository's `AGENTS.md` for version formats, refresh commands, and validation. This repository uses `python3 scripts/refresh-plugin-version.py` for the Codex timestamp; the Claude release version changes only for an intended release.
- Keep `skills/`, `hooks/`, scripts, MCP, and app declarations consistent with files that actually exist. Never add secrets or production data to the plugin.
- For a non-default Codex marketplace path, install it first with `codex plugin marketplace add <marketplace-root>` and verify it with `codex plugin marketplace list`.

## Completion

Complete the selected workflow's validation. For persistent installation or refresh, verify the installed plugin with its agent's plugin list. For Claude Code live-directory loading, completion means manifest validation and loading the directory in a new session. For Codex, validate again if manifest or layout files changed, and tell the user to start a new thread after reinstalling to load updated skills, hooks, or tools. Restart Claude Code after updating a persistent installation.
