"""Accounting and ingestion regressions; synthetic logs only, no private session data."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from extract_sessions import extract, extract_many


def event(kind, **values):
    return {"type": "event_msg", "timestamp": "2026-01-01T00:00:00Z",
            "payload": {"type": kind, **values}}


def token(value, last=None):
    usage = {"input_tokens": value, "cached_input_tokens": 0,
             "output_tokens": 10, "total_tokens": value + 10}
    return event("token_count", info={"total_token_usage": usage,
                                     "last_token_usage": usage if last is None else last})


def prompt(text):
    return {"type": "response_item", "payload": {"type": "message", "role": "user",
            "content": [{"type": "input_text", "text": text}]}}


def meta(thread_id="root", **values):
    return {"type": "session_meta", "payload": {"id": thread_id, "source": "vscode", **values}}


def ordered(records):
    return [{**r, "ordinal": i} for i, r in enumerate(records)]


class AccountingTests(unittest.TestCase):
    def parse(self, records, **kwargs):
        raw = "\n".join(json.dumps(r) for r in records)
        with patch.object(Path, "open", mock_open(read_data=raw)):
            return extract(Path("fixture.jsonl"), **kwargs)

    def test_multiturn_delta_and_duplicate_snapshots(self):
        rows = [event("task_started", turn_id="a"), prompt("first"), token(100), token(100),
                event("task_complete", turn_id="a"), event("task_started", turn_id="b"),
                prompt("second"), token(250), event("task_complete", turn_id="b")]
        turns = self.parse(rows)["turns"]
        self.assertEqual([t["usage_delta"]["input_tokens"] for t in turns], [100, 150])
        self.assertIsNone(turns[0]["usage_delta"]["cache_write_input_tokens"])

    def test_unknown_baseline_and_reset(self):
        rows = [event("task_started"), prompt("question"), token(100, {"input_tokens": 20}),
                event("task_complete")]
        self.assertIsNone(self.parse(rows)["turns"][0]["usage_delta"])
        rows = [event("task_started"), token(100), token(50), event("task_complete")]
        self.assertIsNone(self.parse(rows)["turns"][0]["usage_delta"])

    def test_aborted_and_prompt_filter(self):
        rows = [event("task_started"), prompt("# AGENTS.md instructions target"),
                prompt("actual question"), token(100), event("turn_aborted")]
        self.assertEqual(self.parse(rows, keyword="target")["turns"], [])
        self.assertEqual(self.parse(rows, keyword="actual")["turns"][0]["status"], "aborted")

    def test_tool_overlap(self):
        def tool(kind, cid, second):
            return {"type": "response_item", "timestamp": f"2026-01-01T00:00:0{second}Z",
                    "payload": {"type": kind, "call_id": cid}}
        rows = [event("task_started"), tool("function_call", "a", 1),
                tool("custom_tool_call", "b", 2), tool("function_call_output", "a", 4),
                tool("custom_tool_call_output", "b", 5), event("task_complete")]
        result = self.parse(rows)["turns"][0]
        self.assertEqual(result["tool_response_sum_s"], 6)
        self.assertEqual(result["tool_response_union_s"], 4)

    def test_inherited_metadata_and_history_are_not_child_work(self):
        rows = ordered([meta("child", source={"subagent": {"thread_spawn": {
            "parent_thread_id": "root"}}}, session_id="root", parent_thread_id="root",
            thread_source="subagent", subagent_history_start_ordinal=5),
            meta("root"), event("task_started", turn_id="parent-turn"), prompt("inherited"),
            event("task_complete", turn_id="parent-turn"),
            event("task_started", turn_id="child-turn", root_turn_id="parent-turn"),
            {"type": "response_item", "payload": {"type": "agent_message", "author": "/root",
             "content": [{"type": "input_text", "text": "delegated research"}]}},
            event("task_complete", turn_id="child-turn")])
        result = self.parse(rows, sources=["subagent"], keyword="delegated")
        self.assertEqual(len(result["turns"]), 1)
        turn = result["turns"][0]
        self.assertEqual((turn["session_id"], turn["thread_id"], turn["turn_id"]),
                         ("root", "child", "child-turn"))
        self.assertEqual(turn["user_text"], [])
        self.assertEqual(self.parse(rows, keyword="inherited")["turns"], [])

    def test_explicit_thread_source_selection(self):
        for header, expected in [
            (meta(thread_source="user"), "root"),
            (meta(source={"subagent": {"thread_spawn": {}}}), "subagent"),
            (meta(source={"subagent": {"other": "guardian"}}, thread_source="guardian_review"), "guardian"),
            (meta(source="unrecognized-client"), "unknown"),
        ]:
            with self.subTest(source=expected):
                rows = [header, event("task_started", turn_id="a"), prompt("same"),
                        event("task_complete", turn_id="a")]
                self.assertEqual(self.parse(rows, sources=[expected])["turns"][0]["source"], expected)
                excluded = "guardian" if expected == "root" else "root"
                self.assertEqual(self.parse(rows, sources=[excluded])["turns"], [])

    def test_modern_turn_meter_precedes_unverifiable_cumulative_baseline(self):
        rows = [meta(), event("task_started", turn_id="a"), prompt("question"),
                token(1000, {"input_tokens": 30}),
                {"type": "token_usage_record", "payload": {"thread_id": "root", "turn_id": "a",
                 "response_id": "response-a", "usage": {"input_tokens": 30},
                 "turn_token_usage": {"input_tokens": 50, "cached_input_tokens": 10,
                                      "output_tokens": 5, "total_tokens": 55}}},
                event("task_complete", turn_id="a")]
        turn = self.parse(rows)["turns"][0]
        self.assertEqual(turn["usage_delta"]["input_tokens"], 50)
        self.assertEqual(turn["usage_delta"]["uncached_input_tokens"], 40)
        self.assertIsNone(turn["usage_delta"]["reasoning_output_tokens"])
        self.assertEqual(turn["observed_max_request_input"], 30)
        self.assertEqual(turn["usage_basis"], "recorded_turn_token_usage")


class FileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, rows):
        path = self.root / name
        path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        return path

    def test_compressed_plain_parity_and_corrupt_archive_failure(self):
        plain = self.write("fixture.jsonl", ordered([meta(), event("task_started", turn_id="a"),
            prompt("question"), token(100), event("task_complete", turn_id="a")]))
        compressed = self.root / "fixture.jsonl.zst"
        subprocess.run(["zstd", "-q", "-o", str(compressed), str(plain)], check=True)
        first, second = extract(plain), extract(compressed)
        # File provenance differs; measurements and content must not.
        for result in (first, second):
            result.pop("file")
            result.pop("files")
            for turn in result["turns"]:
                turn.pop("file")
                turn.pop("files")
        self.assertEqual(first, second)
        compressed.write_bytes(b"not a zstandard frame")
        with self.assertRaises(subprocess.CalledProcessError):
            extract(compressed)

    def test_cross_file_merge_preserves_abort_and_incomplete_turn(self):
        rows = ordered([meta(), event("task_started", turn_id="failed"), prompt("failed request"),
                        token(100), event("error", message="recorded failure"),
                        event("turn_aborted", turn_id="failed", reason="error"),
                        event("task_started", turn_id="active"), prompt("still working"), token(150)])
        partial = self.write("partial.jsonl", rows[:4])
        full = self.write("full.jsonl", rows)
        for paths in ([partial, full], [full, partial]):
            results = extract_many(paths, trace=True)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["duplicate_records"], 3)  # Header isn't a work record.
            turns = results[0]["turns"]
            self.assertEqual([t["status"] for t in turns], ["aborted", "incomplete"])
            self.assertEqual([t["usage_delta"]["input_tokens"] for t in turns], [100, 50])
            self.assertEqual(turns[0]["abort_reason"], "error")
            self.assertEqual(turns[0]["errors"][0]["message"], "recorded failure")

    def test_duplicate_history_and_same_prompt_are_different_concepts(self):
        rows = ordered([meta(), event("task_started", turn_id="a"), prompt("repeat"), token(100),
                        event("task_complete", turn_id="a"), event("task_started", turn_id="b"),
                        prompt("repeat"), token(250), event("task_complete", turn_id="b")])
        original = self.write("original.jsonl", rows)
        duplicate = self.write("copy.jsonl", rows)
        result = extract_many([original, duplicate], keyword="repeat")[0]
        self.assertEqual([t["turn_id"] for t in result["turns"]], ["a", "b"])
        self.assertEqual([t["usage_delta"]["input_tokens"] for t in result["turns"]], [100, 150])

    def test_repeated_history_inside_file_is_counted_once(self):
        rows = ordered([meta(), event("task_started", turn_id="a"), prompt("question"), token(100),
                        event("task_complete", turn_id="a")])
        path = self.write("replayed.jsonl", rows + rows)
        result = extract(path)
        self.assertEqual(len(result["turns"]), 1)
        self.assertEqual(result["turns"][0]["usage_delta"]["input_tokens"], 100)

    def test_replayed_tool_identity_does_not_depend_on_capture_timestamp(self):
        rows = ordered([meta(), event("task_started", turn_id="a"),
            {"type": "response_item", "timestamp": "2026-01-01T00:00:01Z", "payload": {
                "type": "function_call", "call_id": "call-a", "name": "read"}},
            {"type": "response_item", "timestamp": "2026-01-01T00:00:02Z", "payload": {
                "type": "function_call_output", "call_id": "call-a", "output": "data"}},
            {**event("task_complete", turn_id="a"), "timestamp": "2026-01-01T00:00:03Z"}])
        copied = [dict(r) for r in rows]
        copied[2]["timestamp"] = "2026-01-01T00:00:01.100Z"
        copied[3]["timestamp"] = "2026-01-01T00:00:02.100Z"
        original = self.write("original.jsonl", rows)
        replay = self.write("replay.jsonl", copied)
        result = extract_many([original, replay])[0]
        self.assertEqual(len(result["turns"]), 1)
        self.assertEqual(result["turns"][0]["tool_rounds"], 1)
        self.assertEqual(result["turns"][0]["tool_response_sum_s"], 1)

    def test_paginated_resume_reuses_ordinals_after_original_abort(self):
        def captured(record, ordinal, second):
            return {**record, "ordinal": ordinal, "timestamp": f"2026-01-01T00:00:{second:02}Z"}
        original = self.write("original.jsonl", [meta(),
            captured(event("task_started", turn_id="old"), 3823, 1),
            captured(prompt("old request"), 3824, 1),
            captured(token(100), 3825, 2),
            captured(event("turn_aborted", turn_id="old", reason="interrupted"), 3829, 3)])
        resumed = self.write("resumed.jsonl", [meta(history_base={
            "thread_id": "root", "end_ordinal_exclusive": 3823}),
            captured(event("task_started", turn_id="new"), 3827, 4),
            captured(prompt("new request"), 3828, 4),
            captured(token(150), 3829, 5),
            captured(event("task_complete", turn_id="new"), 3830, 6)])
        for paths in ([original, resumed], [resumed, original]):
            result = extract_many(paths)[0]
            self.assertEqual(result["warnings"], [])
            self.assertEqual([(t["turn_id"], t["status"]) for t in result["turns"]],
                             [("old", "aborted"), ("new", "complete")])
            self.assertEqual(result["turns"][1]["usage_delta"]["input_tokens"], 50)


if __name__ == "__main__":
    unittest.main()
