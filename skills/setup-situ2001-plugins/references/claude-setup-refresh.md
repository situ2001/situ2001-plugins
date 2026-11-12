# Claude Code setup and refresh

## Live source directory

For local development, validate `.claude-plugin/plugin.json`, then load the live directory in a new session:

```bash
claude plugin validate <plugin-root>/.claude-plugin/plugin.json
claude --plugin-dir <absolute-plugin-root>
```

Use `--plugin-dir` with the source directory to inspect uncommitted local edits directly.

## Persistent installation

Validate `.claude-plugin/marketplace.json` too. Check `claude plugin marketplace list` for an existing registration. Add the repository path (for local changes) or `situ2001/situ2001-plugins` (for published changes) only when that source is not registered. Read the name from the Claude marketplace manifest; it is independent of the Codex personal marketplace name:

```bash
claude plugin marketplace add <plugin-root-or-repository>
claude plugin install situ2001@<claude-marketplace-name> --scope user
claude plugin list
```

## Refresh an existing installation

Refresh its registered marketplace and update the plugin:

```bash
claude plugin marketplace update <claude-marketplace-name>
claude plugin update situ2001@<claude-marketplace-name> --scope user
claude plugin list
```

Use the existing installation scope when updating. The `--scope user` example applies to a user-scope installation; substitute the existing scope for another installation.
