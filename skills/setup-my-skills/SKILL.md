---
name: setup-my-skills
description: Check and refresh my two essential third-party skill sources for Codex, with Claude Code installation when applicable.
---

# Setup My Skills

Manage only these sources in `~/.agents/skills`:

- All skills from `mattpocock/skills`.
- The `herdr` skill from `herdrdev/herdr` ([Herdr installation guide](https://herdr.dev/docs/agent-skill/)).

Use the current `npx skills` CLI. Scope installation to global Codex skills with `--global --agent codex`; the canonical files belong in `~/.agents/skills`. Refresh existing copies from upstream even if they have local edits. This instruction authorizes replacement for the selected agents and removal of upstream-deleted skills from these two sources only, including shared-store cleanup in step 4.

Consider Claude Code installation too: when the user requests it or these sources are already installed for Claude Code, refresh them there as well. Use `--global --agent claude-code` with the same source and skill selections below; Claude Code copies belong in `~/.claude/skills`. For a Codex-only request, keep installation scoped to Codex.

1. Check the installed global skills with `npx skills list --global --json`. Retain this inventory, including source, name, paths, and agent associations, for the cleanup comparison. Do not treat unrelated global skills as candidates for updating.
2. Obtain the current upstream skill names with `npx skills add mattpocock/skills --list` and `npx skills add herdrdev/herdr --list`. The current CLI does not allow `--list` together with `--json`; a fresh upstream checkout and the `name` fields in its `SKILL.md` frontmatter also provide the inventory. Compare the complete Matt collection and only `herdr` from the Herdr source. Establish a complete upstream inventory before marking any installed skill as deleted.
3. Install or refresh the complete Matt Pocock collection and Herdr:

   ```bash
   npx skills add mattpocock/skills --skill '*' --agent codex --global --yes
   npx skills add herdrdev/herdr --skill herdr --agent codex --global --yes
   ```

   If the CLI changes its flags, use its current `--help` and preserve the same source, selection, agent, and global scope. If an add command reports that existing skills were skipped rather than refreshed, run a source-scoped update for those installed skill names. Never run an unscoped global update.
4. After a source refresh succeeds, remove skills recorded under that source in the initial inventory whose names are absent upstream. Use explicit names and selected agents, for example:

   ```bash
   npx skills remove <deleted-skill-name> --global --agent codex --yes
   npx skills remove <deleted-skill-name> --global --agent claude-code --yes
   ```

   Run the Claude Code removal only when it is selected for this refresh. Recheck the installed state: the CLI can retain `~/.agents/skills/<name>` because other agents share it, leaving the deleted skill visible to Codex. For an upstream-deleted managed skill that remains visible, use `npx skills remove <deleted-skill-name> --global --yes` to remove that name from the shared store and all agent links. This shared cleanup is authorized for upstream-deleted managed skills; report when it also removes other agents' links. Preserve unrelated sources. A rename is a new upstream skill installed in step 3 plus an old name removed here. If upstream discovery or refresh fails, leave that source's installed skills in place and report the failure.
5. Verify `npx skills list --global --json` reports the current upstream skills for each selected agent and no upstream-deleted managed skills remain associated with those agents. Each managed skill must have a `SKILL.md` under `~/.agents/skills` and be reachable by Codex. When installing for Claude Code, also verify its agent association and each installed copy's `SKILL.md` under `~/.claude/skills`. Report the number of Matt Pocock skills, the Herdr result, removed names, and any failures for each selected agent. If a command fails, inspect its output and the installed state before retrying.
