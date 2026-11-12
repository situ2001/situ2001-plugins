---
name: situ2001-herdr
description: Dispatch Claude Code or Codex through Herdr with personal startup settings when the user requests a Herdr agent task. Claude uses auto mode; Codex uses yolo mode with an optional explicit or inherited profile.
---

# Situ2001 Herdr

Use this skill to choose an agent and its startup settings, then invoke `$herdr` to perform the requested work.

## Resolve the launch choice

Before creating a pane or starting an agent, resolve the following from the user's request and established conversation choices:

- **Agent:** `claude` or `codex`. If unspecified, ask which one to use.
- **Codex profile (optional):** use the user's explicit profile choice first. If unspecified, try to extract the current profile from established conversation context or the current Codex process's startup arguments (`--profile` or `-p`), inspecting the process ancestry when needed. Preserve the resolved name exactly and pass it as one shell argument. If no profile is established, launch without `--profile` and proceed without asking for a profile. An explicit request to omit a profile takes precedence over inheritance.

An explicit request for both agents launches each with its own settings. A request to continue work with an existing named agent uses that agent; these settings apply to new launches.

## Invoke Herdr and launch

Load and follow the installed `$herdr` skill before issuing Herdr control commands. It owns the environment check, CLI discovery, pane layout, identity and lifecycle handling, prompt submission, and output retrieval. If the dependency is unavailable, report that it must be installed before dispatching.

Follow its sibling-pane workflow in the current tab and working directory, preserving focus with `--no-focus`. Read the pane ID from the creation response and choose a unique live agent name. Supply the native startup arguments after Herdr's `--` separator:

### Claude Code

Launch in auto mode, equivalent to `claude --permission-mode auto`:

```bash
herdr agent start <agent-name> --kind claude --pane <returned-pane-id> -- --permission-mode auto
```

### Codex

When a profile is resolved, launch with it, equivalent to `codex --yolo --profile <profile_name>`:

```bash
herdr agent start <agent-name> --kind codex --pane <returned-pane-id> -- --yolo --profile <profile_name>
```

Otherwise launch with `codex --yolo`:

```bash
herdr agent start <agent-name> --kind codex --pane <returned-pane-id> -- --yolo
```

The angle-bracket values are placeholders; shell-quote actual values when constructing the command. Use the selected mode directly without requesting another confirmation solely for these startup flags.

## Dispatch and return the result

Once Herdr reports the agent ready, submit the user's task through `herdr agent prompt` and follow `$herdr` for waiting and reading the response. Carry the task's scope and constraints into the prompt. Return the agent's conclusion to the user, identifying the agent and any unresolved blocker. Completion requires reading the response, not merely successful prompt submission.
