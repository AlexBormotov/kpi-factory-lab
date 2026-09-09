# Worked example: two completed audits

Most of this kit tells you what to measure. This document shows what the answers look like when
someone actually measures. Two audits were run on the same day against the same checklist: one
against three product repositories, one against the infrastructure the agent sessions themselves
run in. Both are reproduced with every number, verdict and reason intact, and with the identifiers
redacted.

Read the verdict column last. The instructive part is the reason each score came out the way it
did, and in two places the reason turns out to be a defect in the scoring model rather than a
defect in the thing being scored. An audit that cannot produce that result is not an audit.

**De-identification note.** Repository names, product names, vendor names, tool names, file paths
and commit hashes have been replaced with neutral labels. Every number, every verdict and every
piece of reasoning is unchanged from the original measurement.

---

## Part 1. Audit of three repositories

**Measured 2026-08-02 13:40.**

### What was audited

Three repositories owned by one team, audited against the eleven-pillar AI Agent Readiness model
on the L1 to L5 ladder (L1 Functional, L2 Documented, L3 Standardized, L4 Optimized,
L5 Autonomous). A repository level is the minimum across all eleven pillars.

| Label | What it is | State at measurement |
|---|---|---|
| Repository A | A Python service with a device-automation component, driving external targets through an agent | `<sha-a>` |
| Repository B | A Python API service with a relational database and schema migrations | `<sha-b>` |
| Repository C | A TypeScript codebase with a published SDK package and a backend service | `<sha-c>` |

### The measurement

Every row is bound to a commit SHA. **Without that binding the comparison is void**, and this is
not a formality: the working tree moved four times during the day the audit was run. A row that
says "the suite is green" without naming the state it was green in describes a moment that has
already passed. In the original audit each column header carried the SHA of the tree the numbers
were taken from; here those are shown as `<sha-a>`, `<sha-b>` and `<sha-c>`.

Those placeholders are a redaction, not a shortcut, and the distinction matters because the first
lesson at the end of this document is that an unbound row is worthless. In the original record each
column carried a real commit hash. What the placeholder marks is the position where that binding
sat, so that a reader copying this format knows a real one belongs there. A worked example that
quietly dropped the column would have taught the opposite of the lesson it closes with.

Numbers were taken by running the suites and reading the repository, not by asking the team. The
audit table carries only the pillars where something was actually observed in this pass. A dash
means the row was not measured, not that it passed.

### The table

| | Repository A `<sha-a>` | Repository B `<sha-b>` | Repository C `<sha-c>` |
|---|---|---|---|
| Suite | 1662 green, **13 red**, 30 s | **818 green**, 5 skipped, 48 s | **316 green** (228+49+19+20) |
| Pillar 1 Style & Validation | Linter restricted to three undefined-name rules, **placed as a gate, zero findings** | Lint check plus **formatter in the gate**, 312 files clean | Type checker in no-emit mode with strict settings, plus a custom guard |
| Pillar 2 Build System | - | Lockfile present, CI runs on migrations | **Lockfile only in the SDK package**, the backend has none |
| Pillar 3 Testing | Not run in CI | In CI, does not gate merge | In CI, does not gate merge |
| Pillar 5 Dev Environment | - | - | **The standard test command fails in a fresh checkout** |
| Pillar 11 Multi-Agent Coordination | 4 subagents of a single role | 0 | 0 |
| **Level, as first reported** | **L1** (pillar 11) | **L1** (pillar 11) | **L1** (pillar 11) |
| **Level, applying the model's Pillar 11 caveat** | **L1** (pillar 3, suite not in CI) | **L2** | **L3** |

### The verdicts, and why each score is what it is

**As first reported, all three landed on L1, and all three for the same reason: pillar 11.** Under
a plain minimum-across-pillars reading, the weakest pillar sets the level. Two of the three
repositories run no multi-agent coordination at all and have no need for it, and the third runs
four subagents of a single role. So the pillar that did not apply decided the score.

**That report was wrong, and the correction is the most useful thing in this document.** The
scoring model carries a rule for exactly this case, in its Pillar 11 caveat: multi-agent readiness
is opt-in, and where a team does not run multi-agent workloads the pillar is scored honestly and
then marked "Not pursued" and excluded from the minimum. The rule was in the file the whole time.
The audit did not cite the scoring rule it was applying, so nobody noticed that it had applied the
wrong one.

Applying the model as written, the verdicts become the core levels: Repository C at L3,
Repository B at L2, and Repository A held at L1 by pillar 3, its suite not running in CI. Those
are the numbers a reader should act on, and they now agree with the technical ranking in the
paragraph below instead of contradicting it.

**The lesson to take from this is not about pillar 11.** It is that an audit which does not name
the scoring rule it applied produces a number nobody can check, and three identical verdicts in a
row are the shape that failure takes. Write the rule beside the score. This example is left with
both the original verdict and the correction in place, because seeing the correction is worth more
than seeing a clean table.

**By technical core the ranking inverts.** Repository C is L3, Repository B is L2, and
Repository A is held down by a suite that does not run in CI at all. This is the ranking a reader
should act on, which is exactly why the audit reports the core level alongside the minimum level
instead of reporting one number.

**Repository A: 13 red out of 1675, and a gate that found nothing.** The linter is restricted to
three undefined-name rules and is wired as a gate, and it now reports zero findings. Zero findings
after the rule is enforced is a pass, not an absence of evidence, because the same rule found a
live production defect earlier the same day (below). The binding constraint on this repository is
pillar 3: the suite exists, is large, and is not run in CI. A suite that no automation runs is a
detector, not a gate.

**Repository B: 818 green, 5 skipped, and merge is still not gated.** Style and validation are in
the gate, including formatting, across 312 clean files. The build system has a lockfile and CI
runs on migrations. Testing scores lower than it looks: the tests run in CI but do not gate
merge, so the signal is advisory. The 5 skipped tests are worth naming rather than rounding away,
because an unconditional skip is how a suite silently loses coverage.

**Repository C: highest core level, weakest environment.** Type checking runs in no-emit mode with
strict settings plus a custom guard, which is the strongest pillar 1 of the three. It is
undercut by two rows. The lockfile exists only in the SDK package and the backend has none, so
builds of the larger half of the repository are not reproducible. And the standard test command
fails in a fresh checkout, which means the 316 green tests are green only on a machine that has
already been set up by hand. That is a pillar 5 failure and it devalues the pillar 3 number
sitting above it.

**On the suite counts.** Repository C's 316 is reported as its four component runs (228+49+19+20)
rather than as a single total, because a single total hides which component was not run at all.
Repository A's red count is reported next to its green count for the same reason: 1662 green in
isolation reads as health, and 1662 green with 13 red reads as a suite with known live failures.

### The change-size ceiling from the same measurement

The same pass measured change sizes across the three repositories' own histories, because the
ceiling on how large an autonomous change may be is set per repository, not by a single number
for the whole team.

| | Repository A | Repository B | Repository C |
|---|---|---|---|
| Median files per change | 3 | 3 | 7 |
| p75 files per change | 5 | 6 | 12 |

The spread is threefold. A single ceiling would have been wrong for all three. The rule that
follows is: **the ceiling is set at the p75 of the repository's own history.** The ceiling is
neither a target nor a prohibition. A change above it is allowed; it simply loses the right to
ship without a human reading it.

### What moved in one day, across all three

Recorded because it shows what the audit is for. It is not a scorecard, it is a work list.

- **Repository A** went from 93 red to 13 red. A missing async test plugin was restored, a device
  claim lifecycle was fixed, ambient logging context stopped overwriting explicit fields, all
  undefined names were removed and the rule was placed as a gate.
- **Repository B** received its first CI in its history, plus formatting and migrations in the
  gate.
- **Repository C** received a fix to the **rubric**, not to the repository. The audit found the
  scoring wrong, not the code.

### One defect worth naming on its own

It shows the price of a missing pillar 1. A configuration module called a subprocess without
importing the subprocess module. The resulting name error was swallowed, and the memory probe
fell back to a default: it reported **8192 MB on a machine with 49152 MB**. A linter running a
single rule found it in a minute.

Two things are visible in one defect. The failure was silent, so nothing downstream could
distinguish "probed" from "guessed". And the cheapest possible check, one rule, would have caught
it any day of the preceding weeks.

---

## Part 2. Audit of the session infrastructure

**Measured 2026-08-02 12:58.**

### What was audited

The same checklist, applied to the environment the agent sessions themselves run in, treating it
as a repository. The premise being tested is that the factory model applies to the session, not
only to the product: a session has a loop (one turn: context, action, check), a harness
(permissions, tools, memory files, session status), a factory layer (many concurrent sessions in
one working tree), state outside the conversation, and an evidence boundary.

### The measurement

Each row was answered by looking at the running system, not by describing intent: the live session
list, the status sidecar directory, the reviewer processes actually running, and the memory files
present. Verdicts are pass, partial, or fail against the checklist item as written.

### The table

| Checklist item | Fact | Verdict |
|---|---|---|
| Parallel executors are isolated by external resources, not only by files (pillar 11) | **8 active sessions, 3 of them in the same project**, no worktree per session | **fail** |
| Executor status is published and read by neighbours | **1 session out of 8** writes a fresh status, 12% | **fail** |
| The checker has a source of truth independent of what it checks (pillar 11, L5) | **7 live external reviewer processes**, no prompt isolation, confirmed across six attempts | **fail** |
| Measurements are bound to state | Introduced today, absent before | partial |
| Context lives outside the conversation (pillar 4) | Project memory, memory files, a repository-level agent context file | **pass** |
| A rule derived from a defect is written where the next run will read it (pillar 4) | Global rules file, memory files | **pass** |

**Result under the minimum rule: pillar 11 for the session infrastructure is Pre-Functional.**

That is, **the working environment scores worse on this pillar than any of the three product
repositories it maintains.**

### The verdicts, and why each score is what it is

**Isolation: fail.** Eight sessions were active and three of them were working in the same
project, with no worktree per session and a shared git identity. The failure this predicts
happened the same day: one session's commit absorbed a file another session had just written. The
commit is labelled as a documentation change and contains 105 lines of test code. Neither side
knew the other existed. File-level separation was never the question; the shared resources are
refs, stashes, ports, the database, the device and the deployed environment.

**Neighbour observability: fail, and the mechanism existed.** This is the sharpest row in the
audit. The status mechanism was already built. The status command returned "10 sessions running"
and the answer was ignored; no status was published in return. The sidecar directory held a
single file three months old. One session out of eight, 12%, was publishing anything current. A
capability that is present and unused scores the same as a capability that is absent, and the
audit records it that way deliberately.

**Independent checker: fail, with the strongest evidence in the audit.** Seven external reviewer
processes were live concurrently, and under concurrency the reviewer returned answers to prompts
belonging to **other** sessions. This was tested six times, including with an isolated home
directory and an empty working directory, and the behaviour persisted. A checker whose answer may
belong to somebody else's question is not a checker. Note what the six attempts buy: one
occurrence would have been an anomaly, six with isolation attempts is a property of the setup.

**Measurement bound to state: partial.** The binding was introduced on the day of the audit and
did not exist before it. Partial rather than pass, because a control introduced today has no
history behind it. The cost of its absence was already paid: run results were handed over without
a SHA, the tree moved underneath the run, the suite grew from 693 to 740 tests, and the numbers
that had been handed over went stale without anyone noticing.

**Context outside the conversation: pass.** Project memory, memory files and a repository-level
agent context file are present, so the agent does not re-derive the project context on every run.

**Rules from defects are written down: pass.** A rule learned from a defect lands in the global
rules file and the memory files, which is where the next run will read it. The two passing rows
are both pillar 4, and they are the reason the environment functions at all despite the three
failures above them.

**Why the overall verdict is Pre-Functional rather than an average.** Three of six items fail, and
all three are the same pillar. Under the minimum rule the pillar takes the worst of its items,
and below L1 Functional there is only Pre-Functional. Averaging the six rows would have produced a
passing-looking number for an environment in which three separate incidents occurred that day.

### The conclusion this audit produced

All three incidents of the day are precisely the failures pillar 11 exists to catch: a file
absorbed by another session's commit, stale measurements handed over as current, and a checker
answering somebody else's prompt.

The model applies to sessions literally, and on sessions it finds the same three defects it finds
in repositories: an oracle living inside what it checks, an oracle that does not execute, and a
checker with no independent source of truth. One difference matters. A repository has a history
and a gate; a session by default has neither, so the same defects cost more and surface later.

The practical consequence: before raising the maturity of the product repositories above L3, it is
worth raising pillar 11 in the environment that edits them. Otherwise the improvements are being
made by a tool that does not pass its own check.

---

## What this example does not show

Both audits produce the **first** of the two outcomes the method requires: a repository level. Neither
produces the second, the landing decision for one class of change with its nine gates filled in, and
the method is explicit that the second is the one that decides anything.

That is a property of the original engagement rather than an editorial choice: these were readiness
measurements, and no class of change was put forward for unattended landing at the time. Saying so is
better than fabricating a filled gate table, which would be a worked example of a decision nobody
made.

When you run this for a client, expect the second half to take longer than the first. The level comes
from reading the repository. The landing decision comes from arguing about one specific class of
change until nine gates either close or do not, and G4 and G7 are where that argument usually is.

## What to copy from this example

1. **Bind every row to a SHA.** The tree moved four times in one day. An unbound row is a claim
   about a state nobody can return to.
2. **Report the minimum and the core separately.** One number hid the fact that the three
   repositories rank in the exact reverse order by technical core.
3. **Let the audit indict the rubric.** Three identical L1 verdicts produced a fix to the scoring
   model and, in one repository, a fix to the rubric instead of to the code.
4. **Keep the raw counts.** 1662 green reads as health; 1662 green and 13 red reads as a suite
   with known live failures. 316 as four component numbers shows which component did not run.
5. **A dash is not a pass.** Rows that were not measured are marked as not measured.
6. **Score capability that exists but is unused as absent.** The status mechanism was built,
   returned a correct answer, and was ignored. 12% adoption is a failing row.
7. **Audit the environment, not only the product.** The environment scored worse than everything
   it maintains, and that was the finding with the shortest path to action.