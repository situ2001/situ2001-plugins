"""Behavior checks for reminders reconstructed from native session transcripts."""

import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "reminder", Path(__file__).with_name("remind-coding-guidance.py")
)
reminder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reminder)


def usage(tokens, total=9_000_000):
    return {"type": "event_msg", "payload": {
        "type": "token_count", "info": {
            "last_token_usage": {"input_tokens": tokens, "total_tokens": tokens + 100},
            "total_token_usage": {"input_tokens": total},
        }
    }}


def injected(text, role="developer"):
    return {"type": "response_item", "payload": {
        "type": "message", "role": role,
        "content": [{"type": "input_text", "text": text}],
    }}


def marker(tokens="unknown"):
    return f"<!-- situ2001:coding-guidance input_tokens={tokens} -->\n"


def claude_usage(tokens, cached=0, created=0, sidechain=False):
    return {"type": "assistant", "isSidechain": sidechain, "message": {"usage": {
        "input_tokens": tokens, "cache_read_input_tokens": cached,
        "cache_creation_input_tokens": created, "output_tokens": 1000,
    }}}


class ReminderTests(unittest.TestCase):
    def run_hook(self, records=(), event="UserPromptSubmit", source="startup"):
        payload = {"hook_event_name": event, "source": source, "transcript_path": None}
        output = io.StringIO()
        with patch.object(reminder, "transcript_records", return_value=iter(records)), \
                patch("sys.stdin", io.StringIO(json.dumps(payload))), \
                patch("sys.stdout", output):
            reminder.main()
        return output.getvalue()

    def test_startup_always_injects_all_guidance_in_order(self):
        output = self.run_hook(event="SessionStart")
        software_design = (reminder.DOCS / "software-design.md").read_text()
        original_guidance = (reminder.DOCS / "avoid-speculative-defensiveness.md").read_text()
        mutual_trust = (reminder.DOCS / "mutual-trust-and-honest-collaboration.md").read_text()
        self.assertEqual(
            output,
            marker() + software_design + "\n" + original_guidance + "\n" + mutual_trust,
        )

    def test_missing_usage_does_not_remind(self):
        self.assertEqual(self.run_hook(), "")
        self.assertEqual(self.run_hook([injected(marker())]), "")

    def test_initial_context_is_not_counted_as_growth(self):
        self.assertEqual(self.run_hook([injected(marker()), usage(100_000)]), "")

    def test_threshold_and_repeated_intervals_use_last_injection(self):
        records = [injected(marker()), usage(40_000), usage(114_999)]
        self.assertEqual(self.run_hook(records), "")
        records.append(usage(115_000))
        output = self.run_hook(records)
        self.assertTrue(output.startswith(marker(115_000)))
        self.assertIn("Reminder:", output)
        for path in reminder.GUIDANCE:
            self.assertIn(path.read_text(), output)
        records.extend([injected(output), usage(115_001), usage(189_999)])
        self.assertEqual(self.run_hook(records), "")
        records.append(usage(190_000))
        self.assertTrue(self.run_hook(records).startswith(marker(190_000)))

    def test_jump_over_multiple_intervals_reminds_once(self):
        output = self.run_hook([injected(marker(30_000)), usage(300_000)])
        self.assertEqual(output.count("## Avoid Speculative"), 1)

    def test_cumulative_usage_and_cached_subset_are_not_added(self):
        row = usage(50_000)
        row["payload"]["info"]["last_token_usage"]["cached_input_tokens"] = 50_000
        self.assertEqual(self.run_hook([injected(marker(10_000)), row]), "")

    def test_modern_codex_usage_records(self):
        records = [injected(marker(20_000)), {"type": "token_usage_record", "payload": {
            "usage": {"input_tokens": 95_000},
            "thread_token_usage": {"input_tokens": 999_999},
        }}]
        self.assertTrue(self.run_hook(records).startswith(marker(95_000)))

    def test_codex_compaction_discards_previous_usage(self):
        records = [injected(marker(20_000)), usage(120_000), {"type": "compacted"}]
        self.assertEqual(self.run_hook(records), "")
        output = self.run_hook(records, event="SessionStart", source="compact")
        self.assertTrue(output.startswith(marker()))
        records.extend([injected(output), usage(15_000), usage(89_999)])
        self.assertEqual(self.run_hook(records), "")
        records.append(usage(90_000))
        self.assertTrue(self.run_hook(records).startswith(marker(90_000)))

    def test_compact_and_clear_never_reuse_stale_context_tokens(self):
        for source in ("compact", "clear"):
            with self.subTest(source=source):
                output = self.run_hook([usage(150_000)], event="SessionStart", source=source)
                self.assertTrue(output.startswith(marker()))

    def test_resume_resets_reminder_interval(self):
        output = self.run_hook([usage(200_000)], event="SessionStart", source="resume")
        self.assertTrue(output.startswith(marker(200_000)))
        self.assertEqual(self.run_hook([injected(output), usage(210_000)]), "")

    def test_user_quotes_and_tool_outputs_do_not_reset_interval(self):
        records = [injected(marker(20_000)), usage(95_000),
                   injected(marker(95_000), role="user"),
                   {"type": "response_item", "payload": {
                       "type": "function_call_output", "output": marker(95_000)}}]
        self.assertTrue(self.run_hook(records).startswith(marker(95_000)))

    def test_claude_cache_tokens_and_native_hook_attachments(self):
        records = [{"type": "attachment", "attachment": {
            "type": "hook_success", "hookEvent": "SessionStart", "stdout": marker(),
        }}, claude_usage(10_000, cached=20_000),
            claude_usage(15_000, cached=80_000, created=10_000)]
        output = self.run_hook(records)
        self.assertTrue(output.startswith(marker(105_000)))
        records.extend([{"type": "attachment", "attachment": {
            "type": "hook_additional_context", "hookEvent": "UserPromptSubmit",
            "content": [output],
        }}, claude_usage(10_000, cached=100_000)])
        self.assertEqual(self.run_hook(records), "")

    def test_claude_compaction_and_subagent_usage(self):
        records = [claude_usage(100_000), {"type": "system", "subtype": "compact_boundary"},
                   claude_usage(10_000), claude_usage(200_000, sidechain=True)]
        self.assertEqual(self.run_hook(records), "")

    def test_decreased_context_does_not_trigger_reminder(self):
        self.assertEqual(self.run_hook([injected(marker(90_000)), usage(50_000)]), "")

    def test_nullable_token_count_info(self):
        records = [usage(10_000), {"type": "event_msg", "payload": {
            "type": "token_count", "info": None,
        }}]
        self.assertEqual(self.run_hook(records), "")

    def test_transcript_accepts_valid_tail_and_ignores_partial_tail(self):
        for tail in ("", '{"type":'):
            with self.subTest(tail=tail), patch.object(
                    Path, "open", return_value=io.StringIO(json.dumps(usage(10_000)) + "\n" + tail)):
                self.assertEqual(list(reminder.transcript_records("session.jsonl")), [usage(10_000)])
        with patch.object(Path, "open", return_value=io.StringIO(json.dumps(usage(10_000)))):
            self.assertEqual(list(reminder.transcript_records("session.jsonl")), [usage(10_000)])

    def test_malformed_complete_record_is_reported(self):
        with patch.object(Path, "open", return_value=io.StringIO("{broken}\n")):
            with self.assertRaises(json.JSONDecodeError):
                list(reminder.transcript_records("session.jsonl"))

    def test_new_session_without_transcript(self):
        self.assertEqual(list(reminder.transcript_records(None)), [])
        with patch.object(Path, "open", side_effect=FileNotFoundError):
            self.assertEqual(list(reminder.transcript_records("new-session.jsonl")), [])


if __name__ == "__main__":
    unittest.main()
