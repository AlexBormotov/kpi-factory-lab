# The repository standard, tied to what each file earns

A file checklist is not a delivery system. Most repository standards list what must exist and stop
there, which leaves the only question that matters unanswered: what does a change earn by the
existence of these files. Every row below names the gate it feeds. A file that feeds no gate is
hygiene, worth having, but it buys no autonomy.

## The tree

| Path | Level | Feeds |
| --- | --- | --- |
| `.agents/skills/<name>/SKILL.md` | MUST | harness, G5. Vendor-neutral procedures |
| `.claude/skills` | MUST | symlink to `../.agents/skills`, never a second copy |
| `.claude/settings.json` | SHOULD | harness, G5. Permissions, MCP, plugins |
| `.claude/hooks/` | SHOULD | G5 and G8. Approval gates, logged allow and block with timestamps |
| `.claude/agents/` | SHOULD | review subagents |
| `.github/workflows/ci.yml` | MUST | G4 and G7. Separate lint, test, build, review, secret scan, dependency scan |
| `.github/CODEOWNERS` | MUST | G7. Every path has an owner, so every gate has a named human |
| `.github/dependabot.yml` | SHOULD | pillar hygiene |
| `intent.md`, `spec.md`, `plan.md` | MUST | G1 and G6. The approval chain, see below |
| `AGENTS.md` | MUST | the working agreement, vendor-neutral |
| `CLAUDE.md` | MUST | wiring only, imports `AGENTS.md`, never duplicates it. Kept under one page |
| `REVIEW.md` | MUST | G7. What review is, who is required, what a reviewer may not waive |
| `CONTEXT.md` | SHOULD | pillar 4 and the vocabulary gate. Domain glossary, canonical terms |
| `README.md` | MUST | humans: run it, test it, own it, where the dashboards are |
| `evals/` | MUST | G4. See the eval section |
| `.env.example` | MUST | every variable, no values |
| `Makefile` | MUST | G4. One command per task, and CI runs the same command a contributor runs |
| `.gitignore` | MUST | generated files, local secrets, dependencies |
| `.mcp.json` | OPTIONAL | committed MCP servers, reproducible tooling |

**The symlink rule earns its own line.** `.claude/skills` points at `.agents/skills`. The moment it
becomes a second copy, the two drift, and a reader cannot tell which one the agent loaded. We have
made this mistake on our own machines: four copies of the same agent definition across four
repositories, and a two-copy method skill that diverged by two lines without anyone noticing.

**The Makefile rule earns its own line too.** CI running the same command a contributor runs locally
is not a convenience, it is an oracle property. Two different commands means the green a contributor
sees and the green CI sees are different claims.

## The approval chain before code

Three artifacts, each committed, each approved by a named human before the next begins.

| Artifact | Written by | Approved by | Gate |
| --- | --- | --- | --- |
| `intent.md` | originator with an agent | product owner | nothing proceeds without it |
| `spec.md` | agent, guided by repository skills | product owner, tech lead if higher risk | G1: is the task bounded, with a checkable completion condition |
| `plan.md` | agent in plan mode | engineer | G6: the diff is later compared against this |

The value is not the paperwork. It is that G6 evidence becomes checkable: an explanation bound to a
committed plan can be compared to the diff, while an explanation written after the fact cannot.

## Evals: the harness needs its own regression suite

The harness is the work, so the harness needs tests. Otherwise a one-line edit to `CLAUDE.md` or a
skill silently changes behaviour across every future session, and nothing catches it.

- **Baseline:** 20 to 50 real tasks taken from recent work in this repository. Not synthetic ones.
- **Trigger:** the suite runs on any change to `CLAUDE.md`, `AGENTS.md`, `.agents/skills/`, or
  `.claude/hooks/`, and the change is gated on a pass-rate threshold.
- **Growth:** every production incident becomes a permanent eval. The suite only grows.

This is the piece most repository standards miss entirely. A coverage threshold measures the product.
An eval suite measures the factory.

## Coverage thresholds are a quantity, not a proof

A coverage number says how much code a test run touched. It does not say whether anything would have
gone red had the behaviour broken. Require both:

- a coverage threshold that fails the build, and
- **the negative control**: break one behaviour on purpose, and exactly the tests covering it go red
  and no others. Without that, green means the pipeline ran.

## Closing the loop

G9 stops the line and restores green. That is containment, not learning. The loop closes when the
failure re-enters planning:

1. Deterministic monitoring detects a breach of a control band.
2. Response tiers live in version-controlled config: log only, diagnose read-only, propose or act.
3. The diagnosis is written as an `intent.md` and re-enters the chain at the top.
4. The service owner triages. The triage decision is recorded in version control.

## Metrics, leading and lagging

Without these the conversation a month later is about impressions.

| Stage | Leading | Lagging |
| --- | --- | --- |
| Intent | time from first conversation to committed `intent.md` | share of `intent.md` surviving to spec |
| Spec | elapsed time between `intent.md` and `spec.md` | requirements rework after build starts |
| Build | share of changes merging on the first implementation pass | rework cycles per change |
| Test | first-pass CI success rate for agent-written changes | change failure rate from the incident tracker |
| Land | time to first review | defects caught before merge against those escaping |
| Operate | time from breach to a triaged `intent.md` | share of findings that become merged fixes |

Take the baseline before changing anything. A measurement started after the change proves nothing.

## What this standard still does not measure

Comprehension debt: the gap between how much code exists and how much of it the team understands. No
file in the tree measures it and no metric in the table captures it. Say so out loud rather than
implying the checklist is complete.

## Sources and attribution

The stage chain and the harness-regression rules in this file are derived from "The AI-Native SDLC
Playbook", published by Anthropic on 21 August 2026, read on 2026-08-25. The elements taken are:
the committed artifact chain of intent, specification and plan with a named human approving each
before the next begins; the rule that a plan is committed so the diff can later be compared against
it; continuous evaluations in CI gated on a pass rate; the trigger that any change to the instruction
files, skills or hooks runs that suite; the baseline of 20 to 50 real tasks drawn from recent work in
the same repository; the rule that a production incident becomes a permanent evaluation; hooks acting
as approval gates with allow and block decisions logged with a timestamp; the position that the agent
has no route to push to trunk and may act up to the production gate but not through it; a written
review policy as its own file; the closing loop in which a monitored breach is written as a new intent
and re-enters the chain at the top; and the per-stage split of leading and lagging metrics.

The file tree, the requirement levels and the tool-selection rule are derived from a repository
standards document reviewed on 2026-08-25, de-identified per the policy in `README.md`. The elements
taken are: the vendor-neutral skills directory with a runtime-specific directory symlinked to it and
never copied; separate lint, test, build and review jobs with branch protection; ownership rules
covering every path; one command per task with continuous integration running the same command a
contributor runs; a complete environment template carrying no values; and the rule that the tool
endorsed by the framework wins unless there is a documented reason to override it.

Not from either source, and belonging to this kit: binding every row of the tree to the gate it feeds
and stating that a file feeding no gate buys no autonomy; the negative control standing beside the
coverage threshold, and the argument that a coverage number measures the product while an evaluation
suite measures the factory; the reasoning that a single command shared by contributor and pipeline is
an oracle property rather than a convenience, because two commands make two different claims; the
drift argument behind the symlink rule; and the closing section naming comprehension debt as
unmeasured by any row of the tree or any metric in the table.

This file names runtime-specific context files, as `04-readiness-model.md` does and for the same
reason: the tree has to say where the agent-facing surface lives.
