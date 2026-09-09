---
name: agentic-factory
description: Decide whether an agent loop may run without a human, set an evidence-based autonomy gate or change-size ceiling, and diagnose why green checks failed to prevent a break. Use for agentic factory, AI factory, software factory, loop engineering, agent-readiness audits, oracle quality, checker independence, and autonomy pilots. Also use when a semantic value crosses repositories or database, API, MCP, settings and UI layers, including field naming or renaming, naming consistency, vocabulary drift, boundary mappings, and one canonical term per contract.
---

# Software factories with agents

An operational method for deciding, on evidence, how much autonomy a specific loop has earned.
It introduces **no new maturity scale**: scoring stays on the existing AI Agent Readiness model
(5 levels, 11 pillars). This tells you WHAT to measure; the scale is unchanged.

The full method, with its sources, the contradictions between them, and a completed audit, is in
`01-method.md` beside this file.

## 1. Three levels. Confusing them is the usual implementation error

| Level | What it is | Unit of work |
|---|---|---|
| **Loop** | one agent doing one job in a circle: gather context, act, check, repeat until a condition | one change |
| **Harness** | the walls around the loop: sandbox, available tools, memory between runs, and the gate that defines done | one session |
| **Factory** | many harnessed loops at once, fed by a queue, admitted to trunk through an enforced update protocol, watched by a recovery loop, a human owning the whole | a stream |

People tune the model when the bottleneck is the harness or the gate. Name the level first.

Rule sets operate on different units and therefore do not compete: `simplicity-ladder` governs one
change (minutes), `cherny-workflow` governs one session (hours), this method governs the stream
(weeks). A rule from one level does not fix a problem at another. Careful individual changes do not
pay down debt accumulated by the stream.

(An optional external addition at the "one change" level is the Karpathy-inspired behaviour
guidelines at `github.com/multica-ai/andrej-karpathy-skills`, published by that organisation and
derived from Andrej Karpathy's public remarks rather than authored by him. Checked 2026-08-21: the
repository holds one rule set, `karpathy-guidelines`, its README states MIT while it carries no
licence file, and the earlier owner path `forrestchang` still redirects to it. This kit does not
bundle them, so that it carries no third-party dependency.)

## 2. The oracle is the only thing that grants autonomy

An **oracle** is a fast, durable check that decides whether the task was done correctly.

A loop's right to run unattended comes from properties of the oracle, not from the quality of the
model. It must be all three at once:

- **cheap** - runs on every change without spending human attention,
- **frequent** - fires inside the short cycle,
- **unfakeable** - typed gates, property tests, invariants, or a reviewer bound to an external source
  of truth and an explicit rubric.

**Back pressure:** grant exactly as much autonomy as you can verify cheaply and reliably, and no
more.

### Four ways an oracle silently stops being one

More common than model failure. These are four observed failure modes; the second, third and fourth
carry the dated measurements below.

1. **The oracle lives inside what the agent edits.** The agent authors both the code and the proof
   of its correctness. Remedy: put the check beyond the candidate's reach - a separate repository,
   holdout scenarios, a partner contract, a real device.
2. **The oracle checks something the consumer never sees.** Verification runs against the full
   artifact while the consumer receives a truncated one. Measured 2026-08-02: an MCP server
   instruction string was 10542 bytes, the client reads the first 2048, so 80% was invisible. The
   tests searched substrings across the whole string and never looked at the limit. Three tool
   names that routing depends on sat past the cut. The test could not fail.
3. **The oracle does not execute.** Measured: 63 of 93 red tests never ran at all because
   `pytest-asyncio` was absent, while the project's own documentation declared it.
4. **The oracle measures a side effect of the repair instead of the goal.** Measured 2026-08-10: a
   watchdog recreated a stalled process supervisor, then proved success by having a canary validate
   a TLS certificate. But the canary was launched by the watchdog itself, and the CLI it used
   silently starts a fresh empty supervisor when none is running. So after a failed relaunch the
   sequence was: kill everything, relaunch fails, canary spawns an empty supervisor, TLS works
   inside it, the watchdog logs that service is restored and exits zero, with not one application
   running. The check was true and the claim was false, because the check measured the symptom that
   had originally been observed rather than the state that was wanted.

   Remedy is a rule about what success may be defined as: **the success criterion must name the
   goal state, not the absence of the original symptom.** Here: the recorded set of applications is
   back online and the backend received fresh data. Note the trap is not carelessness, it is that
   the symptom was the correct thing to measure right up until the repair started destroying state,
   and nothing announces that moment.

Local checks do not compose into a cross-layer oracle. If correctness includes a boundary contract,
test that contract explicitly; otherwise that criterion has no oracle and the absence will not
announce itself.

**How to test an oracle:** disable the behaviour in production code and run. Exactly the tests
about that behaviour must go red, and no others. Without that negative control, green is not
evidence.

## 3. Where the human boundary sits, and why it does not move

Inner loop (agent): explore, diagnose, implement, run checks, report.
Outer loop (human): decide whether the approach is right, verify the diagnosis, approve, own the
consequences.

**The boundary is evidence, not another prompt:** a diff, tests, logs, and a short explanation
tying them to the task condition.

Splitting maker and checker yields **claims, not proofs**. A sub-agent checker on the same model
with the same context returns correlated confidence, not independent verification. A real checker
needs a source of truth outside the artifact it judges: a contract, a browser, a device, a scanner,
a production invariant.

**Why architecture stays human structurally.** Tests answer in seconds; architectural erosion shows
up over weeks. A check can only hold a gate against failures that appear no slower than it
measures. So intent and architecture stay with the human, not "until the model matures".

**Comprehension debt** is the gap between how much code exists and how much anyone understands. A
dark factory does not pay it down; it accrues it as fast as it can, with the suite green throughout.
No pillar of the readiness model measures it.

## 4. Two outcomes from an audit, not one

1. **A repository level** on the existing model: a number, the minimum across pillars. Nothing new.
2. **A binary decision for one workflow**: may this class of change update trunk unattended, under
   what limits. This is a **landing and release gate**, not a maturity level.

The second is granted to a **class of task**, never to a repository. An L5 repository may stay fully
"lit" by policy; an L3 repository may earn autonomy for exactly one narrow class of routine change.

### Nine gates. L3 is necessary and not sufficient

The landing event is **the trunk update**, not the merge. Under review-gated flow that moment is a
merge; under trunk-based development it is the push, and the recovery move after it is a revert.
The gates are written for the landing event, so they hold under both.

| Gate | Passes when | Otherwise |
|---|---|---|
| G1 Scope | one routine bounded task with a checkable completion condition | split it or give it to a human |
| G2 Maturity | repository is at least L3 on the applicable pillars, scored on branching-model-neutral criteria | human landing required: the agent may prepare the candidate and its evidence, nothing more |
| G3 Risk | the path is not auth, billing, a schema or data migration, or a public contract | leave the lights on |
| G4 Oracle | the check is cheap, frequent and unfakeable at once | a human reads the diff, or build a stronger oracle |
| G5 Harness | restricted tools, isolated candidate state, isolated external resources, durable state, recorded base SHA | do not run unattended |
| G6 Evidence | diff, checks, logs and an explanation, all bound to a frozen base SHA and candidate SHA; if trunk moved, rerun on the new candidate | candidate evidence stale or incomplete: return to the inner loop, do not push |
| G7 Independent landing check | either **prevention** (a protected check with an external source of truth passes on the exact candidate SHA before the ref accepts it) or **containment** (protected CI checks the exact pushed SHA, only one uncertified push range exists at a time, and failure triggers G9) | the human becomes the checker before the push. A local pre-push hook alone does not pass: `--no-verify` removes it and it lives on one machine |
| G8 Exposure authority | the principal that lands on trunk cannot, by itself, deploy production or enable a flag | treat the landing as a release and do not do it unattended |
| G9 Outcome and recovery | the exact landed SHA is observed, and on failure the line stops, an ordinary revert restores the last green SHA, and the same checks rerun | post-landing containment not established: no unattended landing |

### Under trunk-based development the guarantee moves, it does not disappear

Direct pushes to trunk are a branching model, not a deficiency. What they remove is the pre-merge
review gate, and four things are usually named as paying for it: a green trunk, checks before the
push, a size ceiling, and shipping unfinished work dark behind a flag. Those four are necessary and
**not sufficient**, because none of them establishes who controls the checker. Add two:

- the checker and the recovery path sit outside the authority of the thing being checked (G7),
- uncertified trunk transitions are serialized, one at a time, and production exposure stays a
  separate authority (G8).

Each of the four is falsifiable, so each gets a receipt:

| Payment | Trigger | Receipt | Status without it |
|---|---|---|---|
| Green trunk | any update to the trunk ref, or a required result for its tip going failed, cancelled, timed out or absent | base SHA, pushed range, suite manifest, run ids, completion status of every required job, and on failure the revert SHA and the restored green SHA | trunk state unknown or trunk red: no new work, push or deploy starts |
| Pre-push checks | any attempted trunk update | observed base SHA, candidate SHA, hook version, commands, exit codes, tool versions | pre-push verification not established: no unattended push |
| Size ceiling | a candidate asks to land unattended | base and candidate SHA, the counting command and its exclusions, changed files, changed lines, the repository ceiling, and the verdict | change-size eligibility not established; over the ceiling means human landing required |
| Dark shipping | the change carries incomplete behaviour | flag key, config source, per-environment defaults, off-path and on-path test results, a runtime read showing off, and who may flip it | dark shipping not established: it may not land unattended |

**The smallest control that actually binds** is not a hook on the developer's machine and not a
pull-request gate. It is a server-side check bound to the exact SHA: push the candidate to a
short-lived preflight ref, require a protected check on it, then fast-forward the same SHA onto
trunk. No pull request, no reviewer, no merge commit, no long-lived branch, so the model is intact,
and the ref still refuses a SHA the suite has not passed.

**Why the line falls at L3 Standardized.** L3 supplies the minimum machinery for cheap, frequent
enforcement on every change: processes defined, documented and *enforced by automation*, with tests,
linters and security checks. It does not establish that the oracle is unfakeable or relevant to this
task; G4 tests those separately. Below L3 the repository lacks the automated enforcement this method
requires for unattended merge.

### What the eleven pillars do not ask

Three gaps worth naming when scoring, as additions to existing pillars rather than new ones:

1. Pillar 4, an L4 item: the share of code changed this quarter and never read by a human is
   measured (comprehension debt).
2. Pillar 3, an L4 item: checks run against the same artifact the consumer receives, accounting for
   truncation, serialization and transport.
3. Pillar 11, an L5 item: the review agent has a source of truth outside the artifact it judges.

## 5. Two ladders, and the size ceiling

| | Simplicity ladder | Maturity ladder (L1-L5) |
|---|---|---|
| Constrains | the **size** of a change | the **right** of a change to leave without a human |
| Applies | before writing code | when trying to land a candidate |

The link runs one way: **the lower the maturity, the stricter the simplicity ladder must be.** At
L1-L2 there is no proof of correctness, so smallness and reversibility are the only protection. At
L4-L5 a large change is acceptable because there is something to check it with.

**Set the ceiling from the repository's own p75, not from a book.** Measured across three
repositories of one team on 2026-08-02: medians of 3, 3 and 7 files; p75 of 5, 6 and 12. A single
number would have been wrong for all three. The ceiling is neither a target nor a prohibition: a
larger change is allowed, it simply loses the right to land without a human reading it.

## 6. Audit checklist, in terms of the existing pillars

Answer each by looking at the repository, not by opinion.

**Pillar 1, Style & Validation**
- [ ] A deterministic correctness validator exists per main language. A documented N/A is fine.
- [ ] It runs automatically and fails on violations.
- [ ] It runs on **every path into the protected branch**. A workflow on a branch anyone can push to
      is a detector, not a gate.

**Pillar 3, Testing**
- [ ] The suite executes fully, with no tests silently skipped by a missing plugin.
- [ ] The declared suite runs against the exact candidate or landed SHA on every path into trunk,
      and failure either refuses the ref or triggers a protected stop-line and restores the last
      green SHA. A notification-only workflow does not count.
- [ ] Checks run against the artifact the consumer receives, not the full internal one.
- [ ] Critical modules have a negative control: disabling the behaviour reds exactly its own tests.
- [ ] Known failures are strict `xfail` with cause, owner and a review date, never a bare skip.

**Pillar 4, Documentation & Agent Context**
- [ ] Project context lives in the repository; the agent does not re-derive it each run.
- [ ] A rule learned from a defect is written where the next run will read it.
- [ ] A value crossing layers uses one canonical term, with only mechanical variants or classified,
      tested boundary mappings. The vocabulary receipt below is present.

**Pillar 7, Security & Governance**
- [ ] Autonomy is tied to reversibility and blast radius by a deterministic rule, not by discretion.
- [ ] Paths with irreversible cost (money, auth, migrations, public contract) are excluded explicitly.
- [ ] A kill switch exists and fails closed.

**Pillar 11, Multi-Agent Coordination**
- [ ] Parallel workers are isolated by external resources, not only by files.
- [ ] The checker has a source of truth outside the artifact it checks.

### Cross-layer vocabulary gate

The unit is **one semantic contract, one canonical term**, not one identifier repeated verbatim
everywhere. This is a Pillar 4 guard and it produces G6 evidence, not G4 autonomy: an agent-authored
inventory can omit a repository or an alias, so it earns a human reading unless a protected schema,
vocabulary manifest, or contract test validates it from outside.

Measured across two repositories on one call path, each pinned to its own commit. One semantic
value, the model an execution runs on, took four distinct shapes, none of which a check confined to
a single layer can see:

- **Two terms on one surface.** The tools that start work accept a field named `llm_model`, while
  the sibling endpoint that lists the permitted values answers with `agent_models` and
  `default_agent_model`. One surface, two names for one thing.
- **A value mapping mistaken for a name mapping.** Helpers existed to resolve model *values* and
  their aliases, and were read as though they reconciled the field *name*. Nothing mapped
  `llm_model` to `agent_model`. The name simply changed as the value crossed.
- **A name that narrows its own value.** The setting was named after one specific vendor in the
  configuration module and in the operator-visible whitelist, while the docstring of the tool that
  reads it states it may hold any vendor's alias. A field that may hold any vendor's model must not
  be named after one of them.
- **A term that stops.** The database column existed, carried by its migration, and the receiving
  API's create schema had no such field at all. The value disappeared before a consumer that was
  meant to receive it, which is a defect rather than an absence.

**Trigger.** A change introduces, renames, or adds another representation of an identifier for the
same semantic value in two or more active layers or repositories.

**Action.** Name the semantic value, its canonical term, its sources and its terminal consumers, and
derive the in-scope repositories from the task requirements and the actual deployment, route, import
or call edges. Cite the evidence for each repository included and for each plausible one excluded as
off-path. A repository manifest is optional.

Trace the candidate through every boundary on those paths: request schemas, serializers, dispatch
payloads, adapters, domain models, repository calls, database models and migrations, response
schemas, and the runtime or display consumers this task touches. Record the identifier at each
boundary and classify it as canonical, mechanical, allowed exception, missing, or defect. A value
that disappears before an intended consumer is a defect, not an absence.

Search each observed identifier and only the casing, separator, singular or plural, and role-modifier
forms that are observed or mechanically derived under a cited rule. `git grep -nE "\bname\b"` returns
nothing in current Git: use `git grep -n -w -F 'name' <sha> -- '*.py'`. While the candidate is
uncommitted add `--untracked`, record `HEAD` plus `git status --short`, and mark the receipt
provisional; repeat at the candidate SHA before unattended merge. Do not invent synonyms from
neighbouring nouns: an agent cannot prove it searched for a name it never saw.

Syntax, cardinality and role modifiers may vary without changing the canonical term: `llm_model`,
`llmModel`, `LlmModel`, `default_llm_model`, `supported_llm_models`. Cite the language rule or
serializer configuration that makes the transformation mechanical.

A different semantic term is allowed only at an immutable external contract, a compatibility surface,
a localized display boundary, or a distinct bounded context. Put the mapping in the narrowest
explicit boundary component (serializer, compatibility adapter, presenter) and test both names there.
For a bounded-context exception, state the different meaning or invariant; local preference does not
qualify. Do not edit historical migrations, and call a historical name inactive only when a later
migration or the current schema proves it off the active path. An assignment or a helper is not an
exception by itself, and neither is a name that narrows the value: a field that may hold any vendor's
model is not named after one vendor.

**Receipt.** The semantic value and its canonical term; sources and terminal consumers; each in-scope
repository with its scope evidence and candidate SHA; each plausible off-path repository with its
exclusion evidence; the exact search commands; and one row per boundary:
`direction | boundary | identifier or missing | classification | file:line | mapping or test`.
Account for every intended boundary. A provisional `HEAD` plus diff receipt cannot authorize an
unattended merge.

**Otherwise.** Status is "vocabulary not reconciled". Do not report the inventory complete and do
not merge unattended.

Local style rules apply only after this gate and do not license a semantic rename at a boundary.

## 7. Apply it to your own session, not only to repositories

A session in which an agent edits someone else's code IS a factory. Loop = one turn; harness =
permissions, tools, memory files, session status; factory = **many concurrent sessions in one
working tree**; evidence boundary = run output bound to a SHA.

**The oracle for your own work is not a test.** It answers "did I run the check I was obliged to
run". The failures here are skipped steps, not bad formatting: did not run it, did not compare, did
not establish ownership, did not save the source.

Layers a factory-of-sessions usually lacks, all four observed on 2026-08-02:

1. **Isolation.** Sessions share a working tree and a git identity. One session's commit swept up a
   file another had just written; it was labelled `docs` and carried 105 lines of test code.
2. **Awareness of neighbours.** The status mechanism existed and went unused: a session listing
   reported ten running sessions and it was ignored.
3. **Binding a measurement to a state.** Results were reported without a SHA. The tree moved
   underneath the run and the numbers silently went stale.
4. **Independence of the checker.** An external reviewer, run concurrently, returned answers to
   *other sessions'* prompts across six attempts, including with an isolated home directory. A
   checker whose answer may belong to someone else's question is not a checker.

Rules that follow, not observations:

- Before the first write to a shared tree: list active sessions and publish your own **with the
  paths you intend to touch**.
- Every measurement carries a SHA and is rechecked afterwards; if it moved, the result is void.
- Accept an external checker's answer only if it contains specifics from the question you asked. A
  reasonable-sounding text on an adjacent topic is not evidence of relevance.
- Authorship is always established, never described as "someone". That is one `git log -S`.

### The oracle for a sentence: type the evidence, not just the result

Measured 2026-08-10: eight false statements to the owner in one session. They looked like eight
different mistakes and were one, an evidence type silently widening into a claim of another type.

| What was observed | What it was turned into |
|---|---|
| A note about a former version | The behaviour of the current one |
| A command that failed to execute | A negative answer about the subject |
| A check that was started | A check that had finished |
| One route unreachable | The whole machine unreachable |
| A log event at time T | The state right now |
| A comment string in a key file | The identity of the key's owner |
| Four ports probed | The whole port space |
| TLS working for the watchdog's own child | The applications running |

The standing rule that should have caught every one of these was known and quoted, and fired zero
times. Worth stating why, because it generalises: a ban on a word is compiled into the runtime (a
hook reads the finished text and rejects the turn), while a four-step mental procedure requires the
author to notice the moment, interrupt themselves, and invent a discriminating check. There is no
`about_to_make_a_claim` event, and the checker and the claimant are the same process. Add the
asymmetry that finishing a turn is free while "unknown" costs another tool call, and every error
lands on the same side: the question looks closed.

Two practices that survive without runtime support:

- **State the type with the result.** Not "there is no internet", but "one ping, one device, one
  address, and the command itself failed to run". The widening becomes visible while writing.
- **A caveat is not a status.** "Confirmed, the check is still finishing in the background" is the
  same defect as claiming it outright: the reader has already acted. If the discriminating check
  has not returned, the only permitted status is unknown.

## 8. What the sources do not answer

Say these out loud rather than papering over them:

- How to resolve a stale test against a real regression. The sources assume the oracle is correct.
- How to measure comprehension debt. The concept is defined, the metric is not.
- What to do on brownfield. Published successes are greenfield or fresh internal products; the
  author of the simplest autonomous loop says plainly he would not run it on an existing codebase.
- Coordinating several agents in one working tree. A worktree isolates files, not shared refs,
  stash, ports, the database, the device, or the deployed stand.
- Who owns the oracle and how its staleness is caught. An oracle is a product with its own defects,
  owner and review date; no source describes this.
