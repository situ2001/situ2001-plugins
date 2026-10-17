#!/usr/bin/env python3
"""Reinject coding guidance every 75K input-context tokens, without state files."""

import json
from pathlib import Path
import re
import sys


INTERVAL = 75_000
DOCS = Path(__file__).resolve().parents[1] / "docs"
GUIDANCE = (
    DOCS / "apply-guidance.md",
    DOCS / "software-design.md",
    DOCS / "avoid-speculative-defensiveness.md",
    DOCS / "mutual-trust-and-honest-collaboration.md",
)
MARKER = re.compile(r"\A<!-- situ2001:coding-guidance input_tokens=(\d+|unknown) -->")


def input_tokens(record):
    """Read request context size, never cumulative session token consumption."""
    kind = record.get("type")
    payload = record.get("payload", {})
    if kind == "token_usage_record":
        return payload["usage"]["input_tokens"]
    if kind == "event_msg" and payload.get("type") == "token_count":
        info = payload.get("info")
        return info["last_token_usage"]["input_tokens"] if info else None
    if kind == "assistant" and not record.get("isSidechain", False):
        usage = record["message"].get("usage")
        if usage:
            # Claude reports cached input separately; Codex includes it in input_tokens.
            return sum(usage.get(key, 0) for key in (
                "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"
            ))
    return None


def hook_contexts(record):
    """Inspect injected messages, excluding user quotes and tool output."""
    if record.get("type") == "response_item":
        payload = record["payload"]
        if payload.get("type") == "message" and payload.get("role") == "developer":
            return [part["text"] for part in payload["content"]
                    if part.get("type") == "input_text"]
    if record.get("type") == "attachment":
        attachment = record["attachment"]
        if attachment.get("hookEvent") in ("SessionStart", "UserPromptSubmit"):
            if attachment["type"] == "hook_success":
                return [attachment["stdout"]]
            if attachment["type"] == "hook_additional_context":
                return attachment["content"]
    return []


def context_position(records):
    current = baseline = None
    for record in records:
        if (record.get("type") == "compacted" or
                (record.get("type") == "system" and
                 record.get("subtype") == "compact_boundary")):
            current = baseline = None

        tokens = input_tokens(record)
        if tokens is not None:
            current = tokens
            if baseline is None:
                # At startup/compaction, the first request establishes context size.
                baseline = tokens

        for context in hook_contexts(record):
            match = MARKER.match(context)
            if match:
                value = match.group(1)
                baseline = None if value == "unknown" else int(value)
                if baseline is None:
                    current = None
    return current, baseline


def transcript_records(path):
    if not path:
        return
    try:
        transcript = Path(path).open(encoding="utf-8")
    except FileNotFoundError:
        # A new session may not have materialized its transcript yet.
        return
    with transcript:
        for line in transcript:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                # The client appends concurrently; leave an unfinished tail for next turn.
                if not line.endswith("\n"):
                    return
                raise


def main():
    payload = json.load(sys.stdin)
    event = payload["hook_event_name"]
    assert event in ("SessionStart", "UserPromptSubmit"), event
    current, baseline = context_position(transcript_records(payload.get("transcript_path")))
    if event == "UserPromptSubmit":
        if current is None or baseline is None or current - baseline < INTERVAL:
            return
    elif payload["source"] in ("compact", "clear"):
        current = None

    position = "unknown" if current is None else str(current)
    print(f"<!-- situ2001:coding-guidance input_tokens={position} -->")
    if event == "UserPromptSubmit":
        print("Reminder: the following coding instructions remain in effect.\n")
    print("\n".join(path.read_text(encoding="utf-8") for path in GUIDANCE), end="")


if __name__ == "__main__":
    main()
