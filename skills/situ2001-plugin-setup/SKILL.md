---
name: situ2001-plugin-setup
description: Install or refresh the situ2001 plugin for Codex and Claude Code from an existing local directory or marketplace.
---

# Situ2001 Plugin Setup

Use this skill to install or refresh the situ2001 plugin for Codex and Claude Code. Follow the requested agent scope; when no agent is specified, consider both agents and refresh existing installations for each.

## Codex initial setup

1. Confirm the plugin root contains `.codex-plugin/plugin.json`, then validate it:

   ```bash
   python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py <plugin-root>
   ```

2. For a directory outside `~/plugins`, expose it at the conventional source location. A symlink keeps the marketplace source live during development:

   ```bash
   mkdir -p ~/plugins
   ln -s <absolute-plugin-root> ~/plugins/<plugin-name>
   ```

   Check an existing path before replacing it.

3. Create or update the default personal marketplace through the scaffold helper, not by hand-editing JSON:

   ```bash
   python3 ~/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py \
     <plugin-name> --path ~/plugins --with-marketplace
   ```

   Preserve existing plugin files; ensure the entry points to `./plugins/<plugin-name>` and includes installation policy, authentication policy, and category.

4. Read `name` from `~/.agents/plugins/marketplace.json` and install from that implicit personal marketplace:

   ```bash
   codex plugin add <plugin-name>@<marketplace-name>
   codex plugin list
   ```

   Do not run `codex plugin marketplace add` for the default `~/.agents/plugins/marketplace.json` marketplace.

## Codex refresh after edits

For a plugin already listed in a local marketplace, read its marketplace name, rotate the cachebuster, and reinstall. Follow the target repository's `AGENTS.md` for its version format and refresh command. For this repository, use `python3 scripts/refresh-plugin-version.py`; otherwise, when no repository convention exists, use the bundled helper below:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/read_marketplace_name.py
python3 ~/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py <plugin-root>
codex plugin add <plugin-name>@<marketplace-name>
```

Start a new Codex thread after reinstalling so updated skills, hooks, or tools are loaded. Validate again if manifest or layout files changed.

## Claude Code setup and refresh

For local development, validate `.claude-plugin/plugin.json`, then load the live directory in a new session:

```bash
claude plugin validate <plugin-root>/.claude-plugin/plugin.json
claude --plugin-dir <absolute-plugin-root>
```

For a persistent installation, validate `.claude-plugin/marketplace.json` too. Check `claude plugin marketplace list` for an existing registration. Add the repository path (for local changes) or `situ2001/situ2001-plugins` (for published changes) only when that source is not registered. Read the name from the Claude marketplace manifest; it is independent of the Codex personal marketplace name. This repository uses `situ2001-plugins`:

```bash
claude plugin marketplace add <plugin-root-or-repository>
claude plugin install situ2001@situ2001-plugins --scope user
claude plugin list
```

For an existing installation, refresh its registered marketplace and update the plugin:

```bash
claude plugin marketplace update <claude-marketplace-name>
claude plugin update situ2001@<claude-marketplace-name> --scope user
claude plugin list
```

Use the existing installation scope when updating. Keep the Claude manifest's release version unchanged unless making an intended release; the Codex timestamp is separate. Restart Claude Code after updating. To inspect uncommitted local edits directly, use `--plugin-dir` with the source directory.

## Boundaries

- Keep `skills/`, `hooks/`, scripts, MCP, and app declarations consistent with files that actually exist.
- Never add secrets or production data to the plugin.
- For a non-default marketplace path, install it first with `codex plugin marketplace add <marketplace-root>` and verify it with `codex plugin marketplace list`.
