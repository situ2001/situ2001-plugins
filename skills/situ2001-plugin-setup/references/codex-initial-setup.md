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

5. Store the local base instructions in `base-instructions.md` under Codex home
   (`$CODEX_HOME`, or `~/.codex` when unset). Use the single `Apply This Guidance`
   anchor:

   ```text
   Follow "Apply This Guidance" and the guidance it introduces, injected by the situ2001 plugin hooks, throughout the task.
   ```

   In that directory's `config.toml`, set the top-level `model_instructions_file`
   to the prompt file's absolute path. This replaces Codex's built-in base
   instructions. Preserve unrelated settings.

   Keep the plugin's `SessionStart` and `UserPromptSubmit` guidance hooks enabled
   and trusted in `/hooks`. Their output supplies the full guidance as developer
   context. Match the anchor to the heading in `hooks/docs/apply-guidance.md`;
   keep the guidance itself in the plugin's `hooks/docs` files.

   Use `codex features list` to confirm that Codex can load the configuration.
