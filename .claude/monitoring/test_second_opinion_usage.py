import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import textwrap
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("usage", HERE / "second_opinion_usage.py")
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)


def codex(inputs=100, outputs=20):
    return json.dumps({"type": "turn.completed", "usage": {
        "input_tokens": inputs, "cached_input_tokens": min(inputs, 80),
        "output_tokens": outputs, "reasoning_output_tokens": min(outputs, 12)}})


class AccountingTests(unittest.TestCase):
    def test_default_journals_are_isolated_by_working_directory(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Path, "cwd", return_value=Path("/project-a")):
                first = usage.state_dir()
            with patch.object(Path, "cwd", return_value=Path("/project-b")):
                second = usage.state_dir()
            self.assertNotEqual(first, second)

    def test_codex_does_not_double_count_subsets(self):
        self.assertEqual(usage.parse_usage("codex", codex())["total_tokens"], 120)

    def test_codex_multiple_turns_are_ambiguous(self):
        self.assertIsNone(usage.parse_usage("codex", codex() + "\n" + codex())["total_tokens"])

    def test_zero_is_known_only_when_reported(self):
        self.assertEqual(usage.parse_usage("codex", codex(0, 0))["total_tokens"], 0)
        self.assertIsNone(usage.parse_usage("codex", "")["total_tokens"])

    def test_claude_uses_latest_cumulative_model_usage(self):
        def event(n):
            return json.dumps({"type": "result", "subtype": "success", "is_error": False,
                "modelUsage": {"model-a": {"inputTokens": n, "outputTokens": 30,
                "cacheReadInputTokens": 40, "cacheCreationInputTokens": 50, "thinkingTokens": 20},
                "model-b": {"inputTokens": 1, "outputTokens": 2,
                "cacheReadInputTokens": 3, "cacheCreationInputTokens": 4}}})
        parsed = usage.parse_usage("claude", event(10) + "\n" + event(20))
        self.assertEqual(parsed["total_tokens"], 150)
        self.assertEqual(parsed["coverage"], "reported")

    def test_claude_main_loop_is_partial(self):
        raw = json.dumps({"type": "result", "usage": {"input_tokens": 10, "output_tokens": 20}})
        self.assertEqual(usage.parse_usage("claude", raw)["coverage"], "partial")
        self.assertIsNone(usage.parse_usage("claude", raw)["total_tokens"])

    def test_cursor_missing_tokens_stay_unknown(self):
        raw = json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "OK"})
        self.assertTrue(usage.parse_usage("cursor", raw)["provider_success"])
        self.assertIsNone(usage.parse_usage("cursor", raw)["total_tokens"])

    def test_agy_notice_and_pretty_envelope(self):
        raw = "Update available\n" + json.dumps({"conversation_id": "test", "status": "SUCCESS",
              "response": "answer", "usage": {"thinking_tokens": 7, "total_input_tokens": 22}}, indent=2)
        parsed = usage.parse_usage("gemini", raw)
        self.assertEqual(parsed["counters"], [{"total_input_tokens": 22, "thinking_tokens": 7}])
        self.assertEqual(parsed["coverage"], "partial")
        self.assertIsNone(parsed["total_tokens"])

    def test_json_inside_answer_is_not_a_terminal_event(self):
        raw = json.dumps({"type": "item.completed", "item": {"text": codex()}})
        self.assertFalse(usage.parse_usage("codex", raw)["terminal"])

    def test_rejects_boolean_negative_and_invalid_subset(self):
        for value in (True, -1, 1.5):
            with self.subTest(value=value), self.assertRaises(ValueError):
                usage.parse_usage("codex", json.dumps({"type": "turn.completed", "usage": {
                    "input_tokens": value, "output_tokens": 10}}))
        with self.assertRaises(ValueError):
            usage.parse_usage("codex", '{"type":"turn.completed","usage":{"input_tokens":1,"cached_input_tokens":2,"output_tokens":1}}')


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_duplicate_finish_rejected_and_private_content_excluded(self):
        run = usage.start(self.root, "codex", "requested-model")
        raw = json.dumps({"type": "item.completed", "item": {"text": "PRIVATE_SENTINEL"}}) + "\n" + codex()
        usage.finish(self.root, run, 0, raw)
        with self.assertRaises(FileExistsError):
            usage.finish(self.root, run, 0, raw)
        self.assertNotIn("PRIVATE_SENTINEL", "".join(p.read_text() for p in self.root.iterdir()))
        self.assertEqual(usage.report(self.root)["groups"][0]["known_tokens"], 120)

    def test_unfinished_and_partial_prevent_complete_total(self):
        for code in (0, 9):
            run = usage.start(self.root, "codex", "test")
            usage.finish(self.root, run, code, codex())
        usage.start(self.root, "codex", "test")
        row = usage.report(self.root)["groups"][0]
        self.assertEqual((row["reported"], row["partial"], row["failed"], row["unfinished"]), (1, 1, 1, 1))
        self.assertEqual(row["known_tokens"], 240)
        self.assertIsNone(row["total_tokens"])

    def test_parallel_writes_have_unique_ids(self):
        def record(_):
            run = usage.start(self.root, "codex", "test")
            usage.finish(self.root, run, 0, codex())
            return run
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            ids = list(pool.map(record, range(16)))
        self.assertEqual(len(set(ids)), 16)
        self.assertEqual(usage.report(self.root)["groups"][0]["total_tokens"], 16 * 120)

    def test_bad_receipt_is_reported(self):
        (self.root / "broken.start.json").write_text("{")
        self.assertEqual(usage.report(self.root)["unreadable_records"], ["broken.start.json"])

    def test_invalid_usage_finishes_as_unknown(self):
        run = usage.start(self.root, "codex", "test")
        receipt = usage.finish(self.root, run, 0, '{"type":"turn.completed","usage":{"input_tokens":-1}}')
        self.assertEqual(receipt["coverage"], "unknown")
        self.assertTrue((self.root / (run + ".finish.json")).exists())

    def test_date_filter(self):
        usage.start(self.root, "codex", "test")
        self.assertEqual(usage.report(self.root, "9999-01-01")["groups"], [])

    def test_oversized_output_is_unknown(self):
        run = usage.start(self.root, "codex", "test")
        receipt = usage.finish(self.root, run, 0, "x" * (usage.MAX_OUTPUT + 1))
        self.assertEqual(receipt["scope"], "invalid_or_oversized_output")
        self.assertIsNone(receipt["total_tokens"])

    def test_failed_provider_result_is_separate_from_exit_code(self):
        run = usage.start(self.root, "claude", "test")
        raw = '{"type":"result","subtype":"success","is_error":true}'
        usage.finish(self.root, run, 0, raw)
        row = usage.report(self.root)["groups"][0]
        self.assertEqual(row["failed"], 1)
        self.assertIsNone(row["total_tokens"])

    def shell(self, code, env=None, stdin=""):
        return subprocess.run(["bash", "-c", code, "test", str(HERE / "capture.sh")],
                              text=True, input=stdin, capture_output=True, cwd=self.root,
                              env={**os.environ, "SECOND_OPINION_STATE_DIR": str(self.root / "journal"), **(env or {})})

    def test_shell_preserves_input_arguments_output_environment_and_exit(self):
        fake = self.root / "fake.py"
        fake.write_text('import os,sys,json\nassert sys.stdin.read()=="prompt\\n"\n'
                        'assert sys.argv[1]=="argument with spaces"\nassert os.environ["CONTEXT"]=="test"\n'
                        'assert os.environ["model"]=="ambient-model"\nassert os.environ["route"]=="ambient-route"\n'
                        'print(' + repr(codex()) + ')\nprint("child-error",file=sys.stderr)\nsys.exit(7)\n')
        result = self.shell('source "$1"; second_opinion_run codex test -- python3 fake.py "argument with spaces"',
                            {"CONTEXT": "test", "model": "ambient-model", "route": "ambient-route"}, "prompt\n")
        self.assertEqual(result.returncode, 7)
        self.assertEqual(result.stdout, codex() + "\n")
        self.assertIn("child-error", result.stderr)
        self.assertEqual(usage.report(self.root / "journal")["groups"][0]["failed"], 1)

    def test_missing_start_storage_prevents_child_call(self):
        blocked = self.root / "blocked"
        blocked.write_text("file")
        result = self.shell('source "$1"; second_opinion_run codex test -- touch called',
                            {"SECOND_OPINION_STATE_DIR": str(blocked)})
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "called").exists())

    def test_finish_failure_preserves_answer_and_does_not_retry(self):
        fake = self.root / "fake.py"
        fake.write_text('from pathlib import Path\nimport os\np=Path("calls")\n'
                        'p.write_text(p.read_text()+"x" if p.exists() else "x")\n'
                        'for p in Path(os.environ["SECOND_OPINION_STATE_DIR"]).glob("*.start.json"): p.unlink()\n'
                        'print("answer")\n')
        result = self.shell('source "$1"; second_opinion_run codex test -- python3 fake.py')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "answer\n")
        self.assertIn("USAGE_UNRECORDED", result.stderr)
        self.assertEqual((self.root / "calls").read_text(), "x")

    def test_all_documented_adapter_commands_emit_one_receipt(self):
        for route, command in (("claude", "claude"), ("codex", "codex"),
                               ("cursor", "cursor-agent"), ("gemini", "agy")):
            with self.subTest(route=route):
                agent = (HERE.parent / "agents" / (route + "-thinking.md")).read_text()
                block = next(b for b in re.findall(r"```bash\n(.*?)```", agent, re.S)
                             if "second_opinion_run" in b)
                # A shell function stands in for the provider; no model request is made.
                envelope = codex() if route == "codex" else json.dumps({
                    "type": "result", "subtype": "success", "is_error": False,
                    "conversation_id": "fixture", "status": "SUCCESS", "usage": {}})
                setup = command + "() { printf '%s\\n' " + "'" + envelope + "'" + "; }\n"
                result = self.shell(setup + textwrap.dedent(block), {"SECOND_OPINION_MONITOR_DIR": str(HERE)})
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, envelope + "\n")
        rows = usage.report(self.root / "journal")["groups"]
        self.assertEqual({r["route"] for r in rows}, set(usage.ROUTES))
        self.assertTrue(all(r["runs"] == 1 and r["unfinished"] == 0 for r in rows))


if __name__ == "__main__":
    unittest.main()
