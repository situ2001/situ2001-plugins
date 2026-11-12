# Codex refresh after edits

For a plugin already listed in a local marketplace, read its marketplace name:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/read_marketplace_name.py
```

Rotate the cachebuster using the target repository's version convention and refresh command from `AGENTS.md`. If no repository convention exists, use the bundled helper:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py <plugin-root>
```

Then reinstall and verify:

```bash
codex plugin add <plugin-name>@<marketplace-name>
codex plugin list
```
