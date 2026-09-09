# Audit checklist

Answer every line by **looking at the repository**. Not by asking the team, not by reading the
documentation, and not from memory of a similar codebase. Where a line asks for a command, run it
and paste what it printed.

The checklist scores against the existing AI Agent Readiness model (5 levels, 11 pillars). It adds
no scale of its own. Only the pillars that decide unattended landing appear here; the remaining
pillars are scored as usual, elsewhere.

For long-running or shared systems, also use the applicable
[harness runtime questions](12-harness-runtime.md#5-audit-questions) and record their receipts.

**Fill the header first.** A row without a SHA is not evidence, because the tree moves.

| | |
|---|---|
| Repository | |
| Commit audited (SHA) | |
| Branch and branching model | trunk-based / review-gated |
| Date and time of measurement | |
| Auditor | |
| Suite command used | |

---

## Pillar 1, Style and validation

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1.1 | Is there a deterministic correctness validator for each main language? A documented N/A is a valid answer. | | |
| 1.2 | Does it run automatically and fail the build on a violation, rather than printing a warning? | | |
| 1.3 | Does it run on **every path into the protected branch**? | | |

On 1.3: a workflow attached to a branch anyone can push to is a **detector, not a gate**. The
question is whether the ref can accept a commit the validator has not passed. Answer it by reading
the branch protection settings, not the workflow file.

## Pillar 3, Testing

| # | Question | Answer | Evidence |
|---|---|---|---|
| 3.1 | Does the suite execute in full, with nothing silently skipped by a missing plugin or an absent dependency? | | |
| 3.2 | Does the declared suite run against the **exact** candidate or landed SHA on every path into trunk? | | |
| 3.3 | On failure, does the ref get refused, or does a protected stop-line fire and restore the last green SHA? | | |
| 3.4 | Do checks run against the artifact the **consumer receives**, accounting for truncation, serialization and transport? | | |
| 3.5 | Do critical modules have a negative control: disabling the behaviour reds exactly its own tests and no others? | | |
| 3.6 | Are known failures strict `xfail` with a cause, an owner and a review date, never a bare skip? | | |

On 3.1: count what ran, not what exists. A suite reporting "green" while a third of it never
executed is the most common way an oracle stops being one. Compare the collected count against the
number of test functions in the tree.

On 3.3: a notification-only workflow does not count. Somebody reading an alert is a human gate, and
the question here is what happens without one.

On 3.5: this is the single highest-value line in the checklist, and the one teams have never done.
Without a negative control, green is not evidence: it is equally consistent with a working system
and with a check that cannot fail.

## Pillar 4, Documentation and agent context

| # | Question | Answer | Evidence |
|---|---|---|---|
| 4.1 | Does project context live in the repository, so the agent does not re-derive it each run? | | |
| 4.2 | When a defect produces a rule, is that rule written where the next run will read it? | | |
| 4.3 | Does a value crossing layers use one canonical term, with only mechanical variants or classified, tested boundary mappings? | | |
| 4.4 | Is the share of code changed this period and never read by a human measured? (comprehension debt) | | |

On 4.4: expect "no". Almost nobody measures it and no pillar of the readiness model asks for it. It
is here because a factory accrues this debt as fast as it can run, with the suite green throughout,
and a client should hear the words before it costs them something.

## Pillar 5, Development environment

| # | Question | Answer | Evidence |
|---|---|---|---|
| 5.1 | Does the declared test command pass in a **fresh checkout**, on a machine nobody has set up by hand? | | |
| 5.2 | Is the dependency set locked, for every package in the repository rather than for some of them? | | |
| 5.3 | Can an agent bring the environment up from what is written down, without asking a person? | | |

On 5.1: run it in a clean container or a fresh clone, not in your working copy. This is the pillar
that decides whether the testing numbers above mean anything: a suite that is green only on a
prepared machine has no bearing on what CI or an agent will see. In the worked example it is the row
that undercut the strongest repository in the set.

## Pillar 7, Security and governance

| # | Question | Answer | Evidence |
|---|---|---|---|
| 7.1 | Is autonomy tied to reversibility and blast radius by a deterministic rule, rather than left to discretion? | | |
| 7.2 | Are paths with irreversible cost excluded explicitly: money, authentication, schema and data migrations, public contracts? | | |
| 7.3 | Is there a kill switch, and does it fail closed? | | |

On 7.3: test it rather than locating it. A switch nobody has pulled is a hypothesis. Pull it in a
non-production environment and confirm what it actually stopped, and what it left running.

## Pillar 11, Multi-agent coordination

| # | Question | Answer | Evidence |
|---|---|---|---|
| 11.1 | Are parallel workers isolated by **external resources**, not only by files? | | |
| 11.2 | Does the checker have a source of truth outside the artifact it judges? | | |

On 11.1: a per-agent working copy isolates files. It does not isolate shared refs, a stash, ports,
the database, a device, or a deployed environment. Name which of those are shared.

On 11.2: a second agent on the same model with the same context returns **correlated confidence,
not independent verification**. Splitting maker and checker without an external source of truth
yields claims, not proofs.

---

## The two outcomes

An audit produces two answers. Recording only the first is the usual mistake, because the first is
the one that sounds like a result and the second is the one that decides anything.

**1. Repository level.** The minimum across the applicable pillars.

This checklist does not compute it. It covers the five pillars that decide unattended landing, and
a level is the minimum across all eleven, so score the remaining pillars on the worksheet in
`04-readiness-model.md` and bring the number back here. Two rules from that file decide the answer
and are easy to skip: each level needs 80% of its items inside a pillar, and Pillar 11 is marked
"Not pursued" and excluded from the minimum where the team runs no multi-agent workloads. Record
which rules you applied, beside the number.

| | |
|---|---|
| Level | L__ |
| Pillar that set it | |
| Pillars marked Not pursued, and why | |
| Scoring rules applied | 80% within level / Pillar 11 excluded / other: |
| What would raise it by one | |

**2. Landing decision, for one class of change.** Granted to a class of task, never to a repository.
An L5 repository may stay fully human-gated by policy; an L3 repository may earn autonomy for
exactly one narrow class of routine change.

| | |
|---|---|
| Class of change | |
| May it update trunk unattended | yes / no |
| Size ceiling (files, lines) | |
| Where the ceiling came from | this repository's own p75, measured: |
| Paths explicitly excluded | |
| Review date for this decision | |

### The nine gates

Every gate must pass for the class of change named above. One failure means the decision is no.

| Gate | Passes when | Verdict | Evidence |
|---|---|---|---|
| G1 Scope | one routine bounded task with a checkable completion condition | | |
| G2 Maturity | at least L3 on the applicable pillars | | |
| G3 Risk | the path is not authentication, billing, a schema or data migration, or a public contract | | |
| G4 Oracle | the check is cheap, frequent and unfakeable at once | | |
| G5 Harness | restricted tools, isolated candidate state, isolated external resources, durable state, recorded base SHA | | |
| G6 Evidence | diff, checks, logs and an explanation, all bound to a frozen base SHA and candidate SHA | | |
| G7 Independent landing check | prevention (a protected check on the exact candidate SHA before the ref accepts it) or containment (protected CI on the exact pushed SHA, one uncertified range at a time, failure triggers G9) | | |
| G8 Exposure authority | the principal that lands on trunk cannot, by itself, deploy production or enable a flag | | |
| G9 Outcome and recovery | the landed SHA is observed, and on failure the line stops, a revert restores the last green SHA, and the checks rerun | | |

On G7: a local pre-push hook alone does not pass. It can be skipped with a flag and it exists on one
machine. The smallest control that actually binds is server-side and bound to the exact SHA.

On G2: L3 is **necessary and not sufficient**. It supplies automated enforcement on every change.
It says nothing about whether the oracle is unfakeable or relevant to this task, which is what G4
tests separately.

### Size ceiling, measured

Set it from this repository's own distribution. Record the command and the output.

| | |
|---|---|
| Command used | |
| Median files per change | |
| p75 files per change | |
| Ceiling adopted | |

A larger change is not forbidden. It loses the right to land without a human reading it.

---

## Auditor's closing note

Three things to write in plain sentences, because they are what the client will act on.

1. **The one thing that would change the most.** Usually a single missing gate, not a programme.
2. **What is being trusted without evidence right now**, stated as a list. This is the part a client
   has never seen written down.
3. **What was not audited**, and why. An audit that does not name its own boundary invites the
   reader to assume it covered everything.
