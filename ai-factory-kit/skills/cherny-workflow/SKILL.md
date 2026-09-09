---
name: cherny-workflow
description: Workflow orchestration rules for coding sessions, reconstructed from Boris Cherny's public posts on how the Claude Code team works (he is a core engineer on Claude Code at Anthropic). Use when starting a multi-step coding task, planning architectural changes, deciding whether to spawn subagents, handling a bug report, or capturing lessons after a user correction. Six rules cover plan-mode default, subagent strategy, self-improvement loop, verification before done, demand elegance, and autonomous bug fixing, plus a tasks/todo.md and tasks/lessons.md convention.
---

# Cherny Workflow Orchestration

Six rules for how a coding agent operates across a session. Companion to behavioral principles like Karpathy guidelines (which cover how the agent thinks about each change). These cover how the agent operates the workflow.

**Tradeoff:** these rules bias toward planning, verification, and capturing learning. They cost some session latency in exchange for fewer surprises, fewer rollbacks, and compounding improvement across sessions. For trivial one-shot tasks, use judgment.

---

## 1. Plan Mode Default

**Plan before non-trivial work. Re-plan on deviation.**

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, STOP and re-plan immediately.
- Use plan mode for verification steps, not just building.
- Write detailed specs upfront to reduce ambiguity.

Reported and unverified, 2026-09-07: one secondary compilation of his posts attributes to a June 2026
interview the position that newer models no longer need a planning step. No primary source for that
statement was found; the rule stands as written until one is.

Mechanics: cycle into plan mode with `Shift+Tab`, or set `defaultMode: "plan"` in `~/.claude/settings.json`. In plan mode tools are read-only and the agent produces a plan; the user approves before any write.

## 2. Subagent Strategy

**Spawn subagents liberally to keep main context clean.**

- Use subagents liberally to keep the main context window clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, throw more compute via subagents.
- One task per subagent for focused execution.

Mechanics: subagents live in `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (user). Each has its own context window. Write a clear `description` field so Claude routes correctly. Restrict `tools:` per subagent to the minimum surface.

## 3. Self-Improvement Loop

**Capture lessons after every correction. Read them at session start.**

- After ANY correction from the user, update `tasks/lessons.md` (or the project's equivalent like `memory/lessons_*.md`) with the pattern.
- Write rules that prevent the same mistake.
- Ruthlessly iterate until mistake rate drops.
- Review lessons at session start for the relevant project.

The point: a correction is data. Capture it. Forgetting the same correction is the most expensive failure mode for autonomous agents.

## 3b. Hold the Decision (repair is not adoption)

An architectural decision stays in force until it is **explicitly** revisited.
Repairing, diagnosing or benchmarking an alternative is a bounded subtask - it
does not select that alternative.

**Counterfactual trigger.** Before the first action that favours an alternative,
ask: *would this action be needed if the current decision definitely stands?*
If no, stop. Either return to the decision, or open an explicit revision:
`new fact -> which original criterion it changes -> full new tradeoff -> confirm`.

"It is already installed / it now works / its CLI is nicer" are not criteria
unless speed of adoption was a selection criterion in the first place.

**Why it needs a mechanical trigger:** drift does not feel like a decision, it
feels like work. Every step is locally sensible; there is no moment of "I am
switching". Attention does not catch it - a checkable question does.

## 4. Verification Before Done

**Never mark a task complete without proving it works.**

- Diff behavior between main and your changes when relevant.
- Ask: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness.
- Show evidence (test output, log line, diff) before claiming done.

If the staff-engineer check returns "no", do another pass. If unsure, verify with evidence.

## 5. Demand Elegance (Balanced)

**Pause on non-trivial changes. Ask if there is a more elegant way.**

- For non-trivial changes, pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."
- Skip this for simple, obvious fixes. Do not over-engineer.
- Challenge your own work before presenting it.

Trigger phrase: "Knowing everything I know now, implement the elegant solution." Forces a post-hoc rethink after the first working version. The first version often reveals the right shape; rebuild on that knowledge.

## 6. Autonomous Bug Fixing

**Given a bug report, just fix it.**

- Do not ask for hand-holding.
- Point at logs, errors, failing tests, then resolve them.
- Zero context switching required from the user.
- Fix failing CI tests without being told how.

Boundary: this assumes the repo is at Standardized level (tests gate merge, CI fails loud, branch protection prevents catastrophe). On an unsafe repo, autonomous fixing is the wrong default.

**Fixing a failing test never means editing the test until it passes.** The agent authors the code
and would then be authoring the proof of its own correctness, which is the first way an oracle stops
being one. If the test is genuinely wrong, that is a separate change with its own reason stated, and
it is not a change to make in the same breath as the fix it unblocks. Say which of the two you are
doing before you touch the file.

---

## Task Management Convention

Two files at `tasks/`:

**`tasks/todo.md`** (per-task, short-lived):

1. Plan First: write the plan with checkable items.
2. Verify Plan: check in with the user before implementing.
3. Track Progress: mark items complete as you go.
4. Explain Changes: high-level summary at each step.
5. Document Results: add a review section at the end.

**`tasks/lessons.md`** (persistent, compounding):

6. Capture Lessons: after corrections, log the pattern and a rule that prevents recurrence.

Adapt file paths to the project's convention if it uses something else (e.g., `memory/lessons_*.md`).

---

## Core Principles

- **Simplicity First.** Every change as simple as possible. Impact minimal code.
- **No Laziness.** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact.** Only touch what is necessary. No side effects, no new bugs.

---

## How to apply

These rules describe agent behavior, not user behavior. Once this skill is loaded:

- Enter plan mode automatically when a task is non-trivial; do not wait for the user to ask.
- Suggest spawning a subagent when work would flood main context (research, multi-file analysis, parallel review).
- After any user correction in this session, propose a `lessons.md` entry capturing the pattern.
- Before claiming a task is done, run the relevant checks and report evidence.
- For non-trivial changes, after the first working version, pause and ask the elegance question.
- For bug reports, attempt the fix end-to-end (find root cause, fix, verify) before asking the user.

If the user's project conventions conflict with any rule (e.g., "no autonomous commits on customer-facing repos"), the project convention wins. These rules are defaults to apply when no project rule overrides them.

---

## Attribution

The practices come from Boris Cherny's public posts on X about how the Claude Code team works:
the thread of 2 to 3 January 2026 (post `2007179832300581177`, 13 tips), the team-sourced thread
of late January 2026 (post `2017742741636321619`, 10 tips), and the follow-up threads of February
2026. Those posts carry plan mode for complex tasks, subagents such as `code-simplifier` and
`verify-app`, a living `CLAUDE.md` updated after every mistake, fixing bugs end to end from logs, and
the rule that giving the agent a way to verify its work multiplies quality.

The form of this file is not his. The six rule names, the `tasks/todo.md` and `tasks/lessons.md`
convention and the "Core Principles" block come from a community restructuring of those threads
that circulated as "Boris Cherny's CLAUDE.md". Checked 2026-09-07 against a transcription of the
team-tips thread and against a dated compilation of his posts: neither contains those names or
files, and the compilation states that his personal `CLAUDE.md` has not been published. An
earlier version of this file said "Original CLAUDE.md by Boris Cherny", which overstated the
source.

Extended here with related Claude Code guidance on plan mode, subagents, hooks and skills, with
rule 3b and the paragraph on never editing a test to make it pass, which are this kit's own.
