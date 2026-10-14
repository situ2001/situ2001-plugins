#!/usr/bin/env python3
"""Read rollout JSONL or JSONL.zst; emit deduplicated turns without image bytes."""

import argparse
import base64
import hashlib
import json
import subprocess
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


FIELDS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens",
          "output_tokens", "reasoning_output_tokens", "total_tokens")


@contextmanager
def rollout_stream(path):
    if path.name.endswith(".jsonl.zst"):
        # Stream with the installed CLI; a corrupt archive must fail the extraction.
        with subprocess.Popen(["zstd", "-dc", "--", str(path)], stdout=subprocess.PIPE,
                              text=True, encoding="utf-8") as process:
            try:
                yield process.stdout
            finally:
                process.stdout.close()
                status = process.wait()
            if status:
                raise subprocess.CalledProcessError(status, process.args)
    else:
        with path.open(encoding="utf-8") as stream:
            yield stream


def source_kind(meta):
    source = meta.get("source")
    subagent = source.get("subagent", {}) if isinstance(source, dict) else {}
    if meta.get("thread_source") == "guardian_review" or (
            isinstance(subagent, dict) and subagent.get("other") == "guardian"):
        return "guardian"
    if meta.get("thread_source") == "subagent" or (
            isinstance(subagent, dict) and "thread_spawn" in subagent):
        return "subagent"
    if meta.get("thread_source") in ("user", "voice_chat") or source in ("cli", "vscode"):
        return "root"
    return "unknown"


def seconds(start, end):
    try:
        return (datetime.fromisoformat(end.replace("Z", "+00:00"))
                - datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds()
    except (AttributeError, TypeError, ValueError):
        return None


def content_text(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(x.get("text", "") for x in content if isinstance(x, dict))


def image_ids(content):
    result = []
    for block in content if isinstance(content, list) else []:
        if block.get("type") != "input_image":
            continue
        url = block.get("image_url", "")
        if isinstance(url, dict):
            url = url.get("url", "")
        if url.startswith("data:") and ";base64," in url:
            try:
                data = base64.b64decode(url.split(",", 1)[1], validate=True)
                result.append({"sha256": hashlib.sha256(data).hexdigest()})
            except ValueError:
                result.append({"warning": "invalid image data URL"})
        else:
            result.append({"reference": url})
    return result


def prompt_text(content):
    """Exclude recognizable injected setup blocks from prompt matching."""
    blocks = content if isinstance(content, list) else []
    return "\n".join(b.get("text", "") for b in blocks
                     if b.get("type") == "input_text" and not b.get("text", "").lstrip().startswith(
                         ("# AGENTS.md instructions", "<environment_context>", "<image ", "</image>")))


def summarize(path, records, meta, baseline, terminal, trace):
    start = records[0]
    contexts = [r["payload"] for r in records if r.get("type") == "turn_context"]
    users = [r["payload"] for r in records if r.get("type") == "response_item"
             and r["payload"].get("role") == "user"]
    delegated = [r["payload"] for r in records if r.get("type") == "response_item"
                 and r["payload"].get("type") == "agent_message"]
    snapshots = [r["payload"]["info"] for r in records
                 if r["payload"].get("type") == "token_count"
                 and r["payload"].get("info")]
    warnings = []
    usage = None
    meters = [r["payload"] for r in records if r.get("type") == "token_usage_record"
              and r["payload"].get("turn_id") == start["payload"].get("turn_id")
              and r["payload"].get("thread_id") == meta.get("id")]
    if meters and meters[-1].get("turn_token_usage") is not None:
        # This meter is already scoped to a turn, including resumed inherited context.
        final = meters[-1]["turn_token_usage"]
        usage = {k: final.get(k) for k in FIELDS}
        usage_basis = "recorded_turn_token_usage"
    elif snapshots:
        usage_basis = "cumulative_token_count_delta"
        first = snapshots[0].get("total_token_usage", {})
        if baseline is None and first and first == snapshots[0].get("last_token_usage"):
            baseline = {k: 0 for k in first}
        final = snapshots[-1].get("total_token_usage", {})
        if baseline is not None:
            usage = {k: final[k] - baseline[k] if k in final and k in baseline else None
                     for k in FIELDS}
            totals = [baseline] + [s.get("total_token_usage", {}) for s in snapshots]
            reset = any(b[k] < a[k] for a, b in zip(totals, totals[1:])
                        for k in FIELDS if k in a and k in b)
            if reset:
                warnings.append("Cumulative counter decreased; usage delta is unknown.")
                usage = None
        else:
            warnings.append("No verified usage baseline; cumulative total is not a turn delta.")
    else:
        usage_basis = None
        warnings.append("No usage snapshot in this turn.")
    if usage and usage.get("input_tokens") is not None:
        inp, cached = usage["input_tokens"], usage.get("cached_input_tokens")
        usage["uncached_input_tokens"] = inp - cached if cached is not None else None
        usage["cache_hit_ratio"] = cached / inp if inp and cached is not None else None
        if cached is not None and cached > inp:
            warnings.append("Cached input exceeds input; inspect metering schema.")
        if all(usage.get(k) is not None for k in ("input_tokens", "output_tokens", "total_tokens")):
            if usage["total_tokens"] != inp + usage["output_tokens"]:
                warnings.append("Total differs from input plus output.")
    calls = [r for r in records if r["payload"].get("type") in
             ("function_call", "custom_tool_call")]
    outputs = {r["payload"].get("call_id"): r for r in records
               if r["payload"].get("type") in ("function_call_output", "custom_tool_call_output")}
    intervals, steps = [], []
    for number, call in enumerate(calls, 1):
        p = call["payload"]
        out = outputs.get(p.get("call_id"))
        offset = seconds(start.get("timestamp"), call.get("timestamp"))
        duration = seconds(call.get("timestamp"), out.get("timestamp")) if out else None
        text = content_text(out["payload"].get("output")) if out else ""
        if duration is not None and offset is not None and duration >= 0:
            intervals.append((offset, offset + duration))
        else:
            warnings.append(f"Tool round {number} has incomplete or invalid timing.")
        step = {"round": number, "name": p.get("name"), "start_offset_s": offset,
                "response_latency_s": duration, "truncation_marker": "truncated" in text.lower()}
        if trace:
            step["recorded_call"] = p.get("input", p.get("arguments"))
        steps.append(step)
    merged = []
    for left, right in sorted(intervals):
        if merged and left <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], right)
        else:
            merged.append([left, right])
    end = terminal or {}
    state = {"task_complete": "complete", "turn_aborted": "aborted"}.get(
        end.get("payload", {}).get("type"), "incomplete")
    if state != "complete":
        warnings.append("Usage is observed partial usage, not a completed-answer cost.")
    models = [{k: c.get(k) for k in ("model", "effort", "service_tier")} for c in contexts]
    request_inputs = [m.get("usage", {}).get("input_tokens") for m in meters] if meters else [
        s.get("last_token_usage", {}).get("input_tokens") for s in snapshots]
    result = {"file": str(path), "session_id": meta.get("session_id", meta.get("id")),
              "thread_id": meta.get("id"), "source": source_kind(meta),
              "recorded_source": meta.get("source"), "thread_source": meta.get("thread_source"),
              "parent_thread_id": meta.get("parent_thread_id"), "agent_path": meta.get("agent_path"),
              "turn_id": start["payload"].get("turn_id"),
              "root_turn_id": start["payload"].get("root_turn_id"), "cwd": meta.get("cwd"),
              "git": meta.get("git"), "contexts": models, "status": state,
              "started_at": start.get("timestamp"), "ended_at": end.get("timestamp"),
              "duration_ms": end.get("payload", {}).get("duration_ms"),
              "time_to_first_token_ms": end.get("payload", {}).get("time_to_first_token_ms"),
              "event_interval_s": seconds(start.get("timestamp"), end.get("timestamp")),
              "user_text": [text for u in users if (text := prompt_text(u.get("content")))],
              "delegated_text": [content_text(m.get("content")) for m in delegated],
              "images": [i for u in users for i in image_ids(u.get("content"))],
              "usage_delta": usage,
              "usage_basis": usage_basis,
              "observed_max_request_input": max((v for v in request_inputs if v is not None), default=None),
              "tool_rounds": len(calls), "tool_response_sum_s": sum(b-a for a, b in intervals),
              "tool_response_union_s": sum(b-a for a, b in merged),
              "trace": steps, "warnings": warnings}
    if trace:
        result["final_answer"] = end.get("payload", {}).get("last_agent_message")
        if result["final_answer"] is None:
            finals = [r["payload"] for r in records if r.get("type") == "response_item"
                      and r["payload"].get("role") == "assistant"
                      and r["payload"].get("phase") == "final_answer"]
            result["final_answer"] = content_text(finals[-1].get("content")) if finals else None
        result["errors"] = [r["payload"] for r in records if r["payload"].get("type") == "error"]
    result["terminal_type"] = end.get("payload", {}).get("type")
    result["abort_reason"] = end.get("payload", {}).get("reason")
    return result


def read_rollout(path):
    meta, records, warnings = {}, [], []
    inherited = 0
    with rollout_stream(path) as stream:
        for number, line in enumerate(stream, 1):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                warnings.append(f"Unparseable JSON at line {number}; metrics may be incomplete.")
                continue
            p = r.get("payload")
            if not isinstance(p, dict):
                continue
            if r.get("type") == "session_meta":
                if not meta:
                    # The first metadata belongs to this file; later metadata can be inherited.
                    meta = p
                continue
            boundary = meta.get("subagent_history_start_ordinal")
            if boundary is not None and r.get("ordinal") is not None and r["ordinal"] < boundary:
                inherited += 1
                continue
            records.append(r)
    if inherited:
        warnings.append(f"Omitted {inherited} inherited records before subagent history boundary.")
    return meta, records, warnings


def summarize_records(path, records, meta, trace):
    active, baseline, latest = [], None, None
    turns, warnings = [], []
    for r in records:
        p = r["payload"]
        kind = p.get("type")
        if kind == "task_started":
            if active:
                turns.append(summarize(path, active, meta, baseline, None, trace))
            active, baseline = [], latest
        if active or kind == "task_started":
            active.append(r)
        if kind == "token_count" and p.get("info"):
            latest = p["info"].get("total_token_usage", latest)
        if kind in ("task_complete", "turn_aborted") and active:
            expected = active[0]["payload"].get("turn_id")
            if p.get("turn_id") and expected and p["turn_id"] != expected:
                warnings.append("Mismatched terminal turn ID; inspect raw boundaries.")
                continue
            turns.append(summarize(path, active, meta, baseline, r, trace))
            active = []
    if active:
        turns.append(summarize(path, active, meta, baseline, None, trace))
    if not turns:
        warnings.append("No supported task boundaries; inspect this log manually.")
    return turns, warnings


def record_identity(record):
    payload = record["payload"]
    kind = payload.get("type")
    if record.get("type") == "token_usage_record" and payload.get("response_id"):
        return ("token_usage_record", payload["response_id"])
    if kind in ("function_call", "custom_tool_call", "function_call_output", "custom_tool_call_output"):
        if payload.get("call_id"):
            return (kind, payload["call_id"])
    if kind in ("task_started", "task_complete", "turn_aborted") and payload.get("turn_id"):
        return (kind, payload["turn_id"])
    if record.get("type") == "response_item" and payload.get("id"):
        return ("response_item", payload["id"])
    # Anonymous records only match when their captured contents and timestamps match.
    return json.dumps({k: v for k, v in record.items() if k != "ordinal"},
                      sort_keys=True, ensure_ascii=False)


def extract_many(paths, cwd=None, keyword=None, trace=False, sources=None):
    """Merge files of the same thread before accounting, then select turns.

    Exact replayed records are counted once. Different payloads remain visible;
    in particular, a partial copy cannot hide a later abort or completion.
    """
    groups = {}
    for path in paths:
        path = Path(path).expanduser()
        meta, records, warnings = read_rollout(path)
        identity = meta.get("id") or str(path.resolve())
        if identity not in groups:
            groups[identity] = {"meta": meta, "files": [], "records": [], "warnings": []}
        group = groups[identity]
        group["files"].append(str(path))
        group["records"].extend(records)
        group["warnings"].extend(warnings)
    results = []
    for group in groups.values():
        unique = {}
        current_turn = None
        for index, r in enumerate(group["records"]):
            p = r["payload"]
            if p.get("turn_id"):
                current_turn = p["turn_id"]
            # Equal text in two turns is two prompts; anonymous events have no proven identity.
            identity = (current_turn, record_identity(r)) if current_turn else (None, index)
            if identity in unique and unique[identity]["payload"] != p:
                group["warnings"].append("Conflicting payloads for one recorded identity; retained both.")
                identity = (identity, json.dumps(p, sort_keys=True, ensure_ascii=False))
            unique.setdefault(identity, r)
        records = list(unique.values())
        # Resumed paginated files can reuse ordinals beyond their history_base.
        # Preserve a single file's order; chronology across files comes from capture timestamps.
        if len(group["files"]) > 1 and all(r.get("timestamp") for r in records):
            records.sort(key=lambda r: (r["timestamp"], r.get("ordinal", -1)))
        elif len(group["files"]) > 1:
            group["warnings"].append("No complete event order across files; retained input order.")
        path = group["files"][0]
        turns, warnings = summarize_records(path, records, group["meta"], trace)
        selected = [t for t in turns
                    if (not sources or "all" in sources or t["source"] in sources)
                    and (not cwd or Path(t.get("cwd") or "").resolve() == Path(cwd).expanduser().resolve())
                    and (not keyword or any(keyword in text for text in
                         t["user_text"] + (t["delegated_text"] if t["source"] == "subagent" else [])))]
        for t in selected:
            t["files"] = group["files"]
        results.append({"file": path, "files": group["files"],
                        "duplicate_records": len(group["records"]) - len(unique),
                        "warnings": group["warnings"] + warnings, "turns": selected})
    return results


def extract(path, cwd=None, keyword=None, trace=False, sources=None):
    return extract_many([path], cwd, keyword, trace, sources)[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--cwd")
    parser.add_argument("--keyword")
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--source", action="append",
                        choices=("root", "subagent", "guardian", "unknown", "all"),
                        help="Select recorded thread sources; repeat to combine (default: all).")
    args = parser.parse_args()
    for result in extract_many(args.files, args.cwd, args.keyword, args.trace, args.source):
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
