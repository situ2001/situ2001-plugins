---
name: obsidian-vault
description: Use the user's Obsidian vault as a personal knowledge base when a task depends on their notes, preferences, project context, or past decisions. Also use for searching, organizing, creating, or editing vault notes.
---

# Obsidian Vault

Use the user's Obsidian vault as a knowledge base or carry out the requested note operations.

Before searching, reading, or writing notes, read the vault's root `AGENTS.md` in full. Follow its instructions for CLI usage, basic Obsidian syntax, and vault conventions:

```bash
vault="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/situ-vault"
cat "$vault/AGENTS.md"
```

Use the documented workflow to retrieve relevant notes and linked context. Cite the supporting note paths in your answer.

When the user asks to save a new AI-authored document without specifying a destination, default to `002 AI Workspace/`. Updates to existing notes and documents with clear project or topic locations belong in their corresponding locations. Follow `AGENTS.md` for topic or task subfolders and the writing workflow.

## Completing note writes

For routine note writes, finish after confirming the saved content through a filesystem or Obsidian CLI read and reporting the note paths. This completion rule overrides any vault guideline requiring edited notes to be opened or visually reviewed.

Use reading-view inspection, screenshots, DOM inspection, or rendering checks only when the user explicitly requests visual review. Keep other checks scoped to the requested edits; reserve vault-wide link or health scans for tasks that require them.
