---
name: setup-situ2001-plugins
description: Install or refresh the situ2001 plugin and its selected third-party skills for Codex and Claude Code.
---

# Setup situ2001 plugins

Use this skill only when explicitly invoked. It has two workflows; run one or both according to the user's request:

- **Third-party skills:** refresh the managed upstream skills in the global agent skill stores.
- **situ2001 plugin:** install or refresh this repository's plugin for Codex and/or Claude Code.

Preserve the requested agent scope. If a request names both workflows, complete both and report them separately.

## Refresh third-party skills

Manage only these source selections:

- All skills from `mattpocock/skills`.
- The `herdr` skill from `herdrdev/herdr` ([Herdr installation guide](https://herdr.dev/docs/agent-skill/)).
- Only the `frontend-design` skill from `anthropics/skills` ([upstream skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design)).

Use the current `npx skills` CLI. Unless the user requests Claude Code or these sources are already installed for Claude Code, scope the refresh to global Codex skills with `--global --agent codex`; Codex's canonical files belong in `~/.agents/skills`. When Claude Code is selected, use `--global --agent claude-code`; its copies belong in `~/.claude/skills`.

Refreshing existing copies from upstream is authorized even when they have local edits. Removal is authorized only for upstream-deleted skills within the managed selections. Do not update unrelated global skills or run an unscoped global update.

1. Record the installed inventory with `npx skills list --global --json`, including source, name, paths, and agent associations. Keep it for cleanup comparison.
2. Establish complete current upstream inventories with:

   ```bash
   npx skills add mattpocock/skills --list
   npx skills add herdrdev/herdr --list
   npx skills add anthropics/skills --list
   ```

   The current CLI does not allow `--list` with `--json`; a fresh upstream checkout and `name` fields in `SKILL.md` frontmatter are valid ways to complete discovery. Compare all Matt skills, only `herdr` from Herdr, and only `frontend-design` from Anthropic before identifying deletions.
3. Install or refresh the selected agents with the matching commands:

   ```bash
   npx skills add mattpocock/skills --skill '*' --agent codex --global --yes
   npx skills add herdrdev/herdr --skill herdr --agent codex --global --yes
   npx skills add anthropics/skills --skill frontend-design --agent codex --global --yes
   ```

   Use `--agent claude-code` for the Claude Code selection. If the CLI reports existing skills were skipped instead of refreshed, use a source-scoped update for those installed names. Preserve the same source, selection, agent, and global scope if flags change.
4. After a source refresh succeeds, remove only names recorded under that source initially and absent from its current upstream inventory. Use explicit names and selected agents:

   ```bash
   npx skills remove <deleted-skill-name> --global --agent codex --yes
   npx skills remove <deleted-skill-name> --global --agent claude-code --yes
   ```

   Run the Claude Code removal only when Claude Code is selected. If a deleted managed skill remains visible through the shared store, use `npx skills remove <deleted-skill-name> --global --yes`; report if this also removes links for another agent. Preserve unrelated sources. Treat a rename as an upstream add plus removal of the old name. If discovery or refresh fails for a source, leave that source in place and report the failure.
5. Recheck `npx skills list --global --json`. Verify that each selected agent has the current managed upstream skills, no upstream-deleted managed skills, and a reachable `SKILL.md` for every managed skill (`~/.agents/skills` for Codex and `~/.claude/skills` for Claude Code). Report counts, Herdr and Frontend Design results, removed names, and failures per selected agent.

## Install or refresh the situ2001 plugin

Follow the requested agent scope. If no agent is specified, consider both Codex and Claude Code and refresh existing installations for each.

Read only the reference for the agent and installation stage being handled:

- **Codex initial installation:** read [references/codex-initial-setup.md](references/codex-initial-setup.md) for source placement, marketplace creation, and installation.
- **Codex refresh after edits:** read [references/codex-refresh.md](references/codex-refresh.md) for cache version rotation and reinstallation.
- **Claude Code installation or refresh:** read [references/claude-setup-refresh.md](references/claude-setup-refresh.md) for live-directory loading or a persistent installation.

Shared requirements:

- Follow the target repository's `AGENTS.md` for version formats, refresh commands, validation, and reinstall order. This repository uses `python3 scripts/refresh-plugin-version.py` for the Codex timestamp; the Claude release version changes only for an intended release.
- Keep `skills/`, `hooks/`, scripts, MCP, and app declarations consistent with files that actually exist. Never add secrets or production data to the plugin.
- For a non-default Codex marketplace path, install it first with `codex plugin marketplace add <marketplace-root>` and verify it with `codex plugin marketplace list`.

Complete the selected workflow's validation. For persistent installation or refresh, verify the installed plugin with its agent's plugin list. For Claude Code live-directory loading, completion means manifest validation and loading the directory in a new session. For Codex, validate again if manifest or layout files changed, and tell the user to start a new thread after reinstalling to load updated skills, hooks, or tools. Restart Claude Code after updating a persistent installation.
