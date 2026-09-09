# Installing the rule sets and second-opinion agents

The eight rule sets in `skills/` are plain markdown files with a small YAML header. Each has a
`name` and a `description`; the agent runtime reads the description to decide when the rule set
applies, and loads the body when it does.

The four files in `agents/` are optional, English-only Claude Code subagents. Each one routes an
explicit second-opinion request through a separate CLI in read-only or plan mode. Runtime-specific
material is isolated in this file, `04-readiness-model.md`, `agents/`, `monitoring/`, and the relevant sections of
`skills/autoresearch/SKILL.md` and `skills/execution-state/SKILL.md`.

## Install the rule sets

Copy the eight directories into the runtime's skills location.

**For everything the person works on**, install for the user:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

**For one repository only**, install into the project so the rules travel with the code and reach
everyone who clones it:

```bash
mkdir -p .claude/skills
cp -R /path/to/AI\ Factory\ Kit/skills/* .claude/skills/
git add .claude/skills && git commit -m "chore: install the AI Factory rule sets"
```

Committing them into the repository is usually the better choice for a client engagement: the rules
then apply to every engineer and every agent run, not only on the machine where someone ran a copy
command.

## Install the second-opinion agents

Claude Code loads user agents from `~/.claude/agents/` and project agents from `.claude/agents/`.
The file format and locations are documented in the official
[Claude Code subagents guide](https://code.claude.com/docs/en/sub-agents).

For the user:

```bash
mkdir -p ~/.claude/agents ~/.claude/monitoring
cp agents/*.md ~/.claude/agents/
cp monitoring/capture.sh monitoring/second_opinion_usage.py ~/.claude/monitoring/
```

For one repository:

```bash
mkdir -p .claude/agents .claude/monitoring
cp /path/to/AI\ Factory\ Kit/agents/*.md .claude/agents/
cp /path/to/AI\ Factory\ Kit/monitoring/{capture.sh,second_opinion_usage.py} .claude/monitoring/
export SECOND_OPINION_MONITOR_DIR="$PWD/.claude/monitoring"
git add .claude/agents .claude/monitoring && git commit -m "chore: install second-opinion agents and monitoring"
```

The adapters require Python 3.9 or later and the shared monitor above. For a project installation,
set `SECOND_OPINION_MONITOR_DIR` to the absolute helper directory before starting the parent
runtime. Keep the export in the project launch environment. Set `SECOND_OPINION_STATE_DIR` to a
separate local journal directory for each isolated client context. Install the same helper version
as the agent files. Before replacing an existing installation, inspect it and preserve local changes.

Read usage with `python3 ~/.claude/monitoring/second_opinion_usage.py report`, or the project
path. Missing and partial counters remain visible; there is no automatic token cutoff. See the
[monitoring guide](monitoring/README.md) for field meanings, storage and verification.

Install and authenticate only the routes the team intends to use. Each agent performs its own
preflight and stops instead of substituting another model or route.

Model identifiers are pinned inside each agent file, with the date they were last probed. When a
vendor ships a newer model, the pin moves only after the probe recorded in that file passes on the
installed CLI. An announcement is not a receipt.

| Agent | Required command | Preflight |
|---|---|---|
| `claude-thinking` | `claude` | `claude auth status` succeeds and the account can use `opus` |
| `codex-thinking` | `codex` 0.153.4 or later | `codex --version` succeeds, the CLI is authenticated, and a pinned probe with the identifier in `agents/codex-thinking.md` completes a turn |
| `cursor-thinking` | `cursor-agent` | `cursor-agent --list-models` succeeds, exposes models for the account, and contains the exact identifier `gpt-5.6-sol` |
| `gemini-thinking` | `agy` | `agy models` contains the selected model and `~/.gemini/antigravity-cli/settings.json` contains only the `read_file(*)` allow rule |

## Confirm they loaded

```bash
ls ~/.claude/skills/          # or ls .claude/skills/
```

Expect eight directories: `agentic-factory`, `autoresearch`, `boundary-dispatch-matrix`,
`cherny-workflow`, `earned-length`, `execution-state`, `grilling`, `simplicity-ladder`.

Then ask the agent to list its available skills, and check that all eight appear by name. A skill
present on disk but missing from that list may have a malformed header: the opening `---` fence
must be the first line, the closing fence must follow the YAML fields, and `name` must match the
directory name.

For the optional agents:

```bash
ls ~/.claude/agents/           # or ls .claude/agents/
```

Expect `claude-thinking.md`, `codex-thinking.md`, `cursor-thinking.md`, and
`gemini-thinking.md`. Restart Claude Code or run `/agents` after changing agent files so the new
definitions are loaded.

## Check that a rule actually fires

Presence on disk is not the same as taking effect, and this is worth two minutes.

| Rule set | Say this | What should happen |
|---|---|---|
| `grilling` | "grill me on this plan: we will move the run loop into a worker process" | it maps the design tree and asks the whole frontier as one numbered round, each question with its own recommended answer, then waits |
| `boundary-dispatch-matrix` | the same sentence, without asking to be grilled | it should demand a filled Boundary/Dispatch Matrix before any code is written |
| `simplicity-ladder` | "should we add a small library for retry with jitter" | it should name which rung it is taking and why the rung above it does not hold |
| `earned-length` | "add explanatory comments to this function" | it should add none by default and name which of the four durable reasons any comment it keeps satisfies |
| `agentic-factory` | "can this repository merge agent changes without review" | it should ask for evidence against the nine gates rather than give a yes or no |
| `autoresearch` | "start an autoresearch run" | it should refuse to consume compute until the checkout, the baseline row and the ledger header are verified |
| `execution-state` | "we are running out of context, summarize the history so we can carry on" | it should refuse summarization as the fix, name the budget-matched controls that failed, and ask for a state schema instead |

If a rule set does not fire, the usual cause is that its `description` was edited. The description is
how the runtime routes to it, so it is functional text and not a summary: rewriting it to read more
nicely will stop it loading.

## Adapting to a different runtime

If the client uses an agent runtime with a different mechanism, the content transfers without
change; only the delivery does. In descending order of preference:

1. **A skills or rules directory**, if the runtime has one. Same files, different path.
2. **The repository instruction file** the runtime reads on every run (`CLAUDE.md`, `AGENTS.md`,
   `.cursorrules` and equivalents). Paste the bodies in, or link to the files from it. Rules are
   long, so linking keeps the instruction file readable.
3. **The system prompt**, for a runtime with neither. Start with `agentic-factory` and
   `simplicity-ladder`: they carry the most weight per line.

One caution when adapting. `cherny-workflow` contains mechanics tied to one runtime's features
(a planning mode, subagents, a settings file). Those paragraphs are the parts to rewrite for another
runtime; the six rules above them are not runtime-specific and should survive unchanged.

## What to hand a client, and what to keep

| Handing over | Include |
|---|---|
| the method, for their architects to read | `README.md`, `01-method.md`, `02-audit-checklist.md`, `03-worked-example.md`, `04-readiness-model.md`, `05-intent-layer.md`, `06-judgement-oracle.md`, `07-human-boundary.md`, `08-measured-loop.md`, `09-build-or-buy.md` |
| a working setup, for their engineers | all of the above plus `skills/`, optional `agents/` with `monitoring/`, and this file |
| an assessment report | your filled-in copy of `02-audit-checklist.md` and the scoring worksheet from `04-readiness-model.md`, never the blank forms alone |

`04-readiness-model.md` is not optional in any of those rows. It is the only file that defines the
five levels and the eleven pillars, so a bundle without it hands someone a method whose first
sentence refers to a scale they do not have.

Keep the blank checklist as the template. A filled checklist is the deliverable, and it is only
worth anything if every answer came from looking at the repository.
