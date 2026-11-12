# Codex initial setup

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
