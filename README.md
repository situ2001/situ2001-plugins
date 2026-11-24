# situ2001-plugins

Personal hooks and skills for Claude Code and Codex, packaged as the `situ2001` plugin.

The Claude Code marketplace is named `situ2001-plugins`; Codex uses the personal marketplace name from `~/.agents/plugins/marketplace.json`. Skills use the `situ2001:` namespace.

## Claude Code

```bash
claude --plugin-dir .
```

Or inside a session: `/plugin` → install from folder.

## Codex

Run this command from a Git checkout with `python3`, `git`, `codex`, and `claude`
on your `PATH` to configure the personal marketplace and install the plugin.

```bash
python3 scripts/refresh-codex-plugin.py --setup-marketplace
```

Review and trust the hooks with `/hooks`. For routine updates, see the
[plugin refresh commands](AGENTS.md#update-and-refresh-the-plugin).

## Coding guidance reminders

`SessionStart` injects a short decision-point prompt from
`hooks/docs/apply-guidance.md`, followed by `hooks/docs/software-design.md`,
`hooks/docs/how-to-design-ui.md`,
`hooks/docs/avoid-speculative-defensiveness.md`,
`hooks/docs/mutual-trust-and-honest-collaboration.md`,
`hooks/docs/english-terminology.md`, and `hooks/docs/clear-writing.md`
in that order at startup,
resume, and after compaction. At each user-turn start, `UserPromptSubmit` reads the
client's transcript and repeats the guidance once the latest request's input
context has grown by 75,000 tokens since the last injection. It uses request input
tokens, including cached input, rather than cumulative session usage. A jump of
several intervals produces one reminder.

The injection includes a position marker that the client saves in its own
transcript. The hook only reads that transcript and prints context; it creates no
state or temporary files. When no usage exists yet, the first recorded request
establishes the baseline. Compaction and `/clear` reset the baseline. Checks run when the user
submits a prompt, so growth within a turn is checked at the next user turn, using
the latest recorded request size; the new prompt and subsequent tool results are
not yet included.

The parser supports Codex JSONL usage/message records and Claude Code
usage/attachment records. These transcript formats are client internals; changes
to them may require updating the parser.
