# Second-opinion token monitoring

Usage accounting lives outside skills. The four adapters call `capture.sh`, which records a start
receipt, runs the existing command, and passes its JSON output to `second_opinion_usage.py` before
the adapter extracts the answer. Python 3.9 or later and Bash are required; no packages or service
are needed. Install both files alongside the agent definitions using [INSTALL.md](../INSTALL.md).

## Read the report

For a user installation:

```bash
python3 "$HOME/.claude/monitoring/second_opinion_usage.py" report --since 2026-09-07
```

For a project installation, use `.claude/monitoring/second_opinion_usage.py` instead. Omit `--since`
to include every recorded run. The date filter uses the run's start date in UTC. Output is JSON,
grouped by route and requested model, with run counts, failures, usage coverage and known tokens.

- `reported`: the supported provider counters are present. This is the provider's reporting scope,
  not proof that every background call was metered.
- `partial`: some counters are present, but their scope, completeness or semantics is limited.
- `unknown`: token consumption cannot be established from the output.
- `unfinished`: a start receipt has no finish receipt. It does not establish that the CLI is still running.
- `known_tokens`: the sum of computable totals. If coverage is incomplete, this is only a subtotal.
- `total_tokens`: populated only when every run in the group has reported usage; otherwise `null`.

A failed run can still consume tokens. Failure count and usage coverage are separate. The report
names unreadable records and exits nonzero when it encounters one. It never counts unreadable data
as a zero-cost run. Each finish receipt retains the allowed numeric counters for inspection.

## Provider coverage

| Route | Counters and accounting scope |
|---|---|
| Claude | Last terminal `modelUsage`, grouped by reported model. Add input, output, cache-read and cache-write counters. Thinking is already in output. Earlier cumulative results are not summed. The main-loop-only `usage` fallback is partial. |
| Codex | One terminal `turn.completed.usage` from the one-prompt adapter. Total is input plus output; cached input and reasoning output are subsets. Multiple terminal turns are marked ambiguous. |
| Cursor | The documented JSON result has no token counters. Record outcome and timing, with token usage unknown. |
| Gemini via `agy` | Retain allowlisted numeric fields from the final envelope's `usage`. Mark them partial and leave the normalized total unknown until this CLI's accounting semantics are verified. |

These values are token telemetry, not invoices, subscription quota remaining, or cross-provider
cost comparisons. Parent-agent `totalTokens` is not a substitute for a child run's usage ledger.

Schemas and semantics: [Claude result and model usage](https://code.claude.com/docs/en/agent-sdk/python),
[Codex JSON events](https://developers.openai.com/codex/noninteractive),
[Codex token accounting source](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs),
[Cursor output schema](https://cursor.com/docs/cli/reference/output-format).

## Storage and lifecycle

Default local journal base directory:

| Platform | Directory |
|---|---|
| macOS | `~/Library/Application Support/ai-factory-kit/second-opinion` |
| Linux | `$XDG_STATE_HOME/ai-factory-kit/second-opinion`, defaulting to `~/.local/state/ai-factory-kit/second-opinion` |
| Windows with Bash | `%LOCALAPPDATA%/ai-factory-kit/second-opinion` |

Within this base, the resolved working directory selects a separate journal using a hash of its
path. Run the report from the same working directory as the second-opinion request. The path itself
is not saved in records. This keeps project journals separate by default.

Set `SECOND_OPINION_STATE_DIR` before launching the parent runtime to select an explicit journal
directory. Keep this override separate for each isolated client context and use the same setting
when reading its report. The Python commands also accept `--state-dir PATH` before the subcommand.

Every invocation gets a UUID and separate `*.start.json` and `*.finish.json` files. Duplicate finish
writes fail rather than double-counting. Parallel invocations use separate files. Records contain
timestamps, collector hash, route, requested model, exit status, usage coverage and numeric counters. They contain
no prompt, answer, working-directory path, environment variables or authentication material.

The shell helper temporarily captures stdout in a private file and removes it on normal shell
exit. Stderr remains visible; the finish receipt is also written there. The helper preserves the
child's stdout, stdin, argument boundaries, working directory, environment and exit code. It does
not add a process timeout, retry, permission override or model fallback. After a forced kill, a
missing finish receipt remains visible as unfinished; abnormal process termination can also leave
a temporary stdout file in the operating system's temporary directory.

Start-record failure prevents the model call. Finish-record failure emits `USAGE_UNRECORDED` and
preserves the original result; never rerun a paid request to repair telemetry. Outputs over 32 MiB
and invalid counters produce unknown usage. Telemetry errors do not become model success.

## Verify or extend

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s monitoring -p 'test_*.py' -v
```

The offline suite checks accounting, missing data, duplicate and concurrent records, privacy and
the shell integration. It makes no model calls. A real provider run is a separate acceptance check:
retain its stderr receipt, compare the allowed counters with the CLI envelope, and confirm that
the same run appears once in `report`. Authentication uses the CLI's existing credential store;
the monitor neither reads nor copies credentials.

To add a schema, obtain the installed CLI's terminal envelope and its official field definitions,
add a fixture and accounting test, and extend only the allowlist and parser. Do not infer cache or
thinking semantics from similar field names. Missing documentation keeps the total unknown.

No hard token ceiling or automatic cancellation is configured. Budget enforcement requires an
explicit limit and a policy for incomplete telemetry. This monitor first makes the measured
consumption and the gaps visible.
