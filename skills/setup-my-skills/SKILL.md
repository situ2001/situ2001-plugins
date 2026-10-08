---
name: setup-my-skills
description: Check and refresh my two essential third-party skill sources for Codex, with Claude Code installation when applicable.
---

# Setup My Skills

Manage only these sources in `~/.agents/skills`:

- All skills from `mattpocock/skills`.
- The `herdr` skill from `herdrdev/herdr` ([Herdr installation guide](https://herdr.dev/docs/agent-skill/)).

Use the current `npx skills` CLI. Scope installation to global Codex skills with `--global --agent codex`; the canonical files belong in `~/.agents/skills`. Refresh existing copies from upstream even if they have local edits. This instruction authorizes replacement of skills from these two sources only.

Consider Claude Code installation too: when the user requests it or these sources are already installed for Claude Code, refresh them there as well. Use `--global --agent claude-code` with the same source and skill selections below; Claude Code copies belong in `~/.claude/skills`. For a Codex-only request, keep installation scoped to Codex.

1. Check the installed global skills with `npx skills list --global --json`. Identify entries from the two sources and confirm their paths. Do not treat unrelated global skills as candidates for updating.
2. Install or refresh the complete Matt Pocock collection and Herdr:

   ```bash
   npx skills add mattpocock/skills --skill '*' --agent codex --global --yes
   npx skills add herdrdev/herdr --skill herdr --agent codex --global --yes
   ```

   If the CLI changes its flags, use its current `--help` and preserve the same source, selection, agent, and global scope. If an add command reports that existing skills were skipped rather than refreshed, run a source-scoped update for those installed skill names. Never run an unscoped global update.
3. Verify `npx skills list --global --json` reports the two sources, each managed skill has a `SKILL.md` under `~/.agents/skills`, and Codex can reach them. When installing for Claude Code, also verify its agent association and each installed copy's `SKILL.md` under `~/.claude/skills`. Report the number of Matt Pocock skills, the Herdr result, and any failures for each selected agent. If a command fails, inspect its output and the installed state before retrying.
