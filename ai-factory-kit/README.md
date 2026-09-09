# AI Factory

An operational method for deciding, on evidence, how much autonomy a specific agent loop has
earned, plus the working rules that hold a coding session together while it runs.

This is not an essay about agentic development. It is the machinery: what to measure, what the
gates are, what evidence closes each gate, and what to do when the checks are green and the system
is broken anyway.

## The problem it addresses

Teams adopting coding agents hit the same wall in the same order. The agent produces plausible
work. The suite is green. Something ships that should not have. The response is usually to tune the
model or add another review step, and neither helps, because the failure was never in the model.

The method is built on one claim, and everything else follows from it:

> A loop's right to run without a human comes from properties of its **oracle**, not from the
> quality of its model.

An oracle is the check that decides whether the work was done correctly. If it is cheap, frequent
and unfakeable, autonomy can be granted. If it is any two of the three, it cannot. Most of this kit
is about the ways an oracle stops being one without announcing it.

## What is in here

| File | What it is | Who reads it |
|---|---|---|
| `01-method.md` | The method in full: the three levels, the oracle, the nine gates, the two ladders, the cross-layer vocabulary gate, and the questions the sources do not answer | the engineer or architect running the assessment |
| `02-audit-checklist.md` | The audit, as questions answered by looking at the repository rather than by opinion | whoever performs the audit, in the repository |
| `03-worked-example.md` | Two completed audits, with the numbers and the reasoning that produced each verdict | anyone who has never seen one filled in |
| `04-readiness-model.md` | The scale everything is scored against: 11 pillars, 5 levels, with the posture that defines each level of each pillar | the assessor, alongside the checklist |
| `05-intent-layer.md` | The upstream layer: the four artifacts that carry intent, the edges between them, the coherence sensor and its calibration order | the architect standing up the layer |
| `06-judgement-oracle.md` | The oracle pattern for tasks whose correctness is a judgement rather than a comparison, with its price and its residual limits | whoever owns an oracle of that class |
| `07-human-boundary.md` | The list of what stays with human judgement, the test that decides it, and how a human gate is told apart from a decoration | the client's engineering leadership |
| `08-measured-loop.md` | Mandatory: the measured-loop protocol and the one-day rehearsal a team owes before any autonomy decision, with a public reference implementation | the engineer running the assessment |
| `09-build-or-buy.md` | How to map a vendor platform to local equivalents with receipts, the filled example, and the five measurements that settle a capability claim | whoever answers the buy-or-build question |
| [12-harness-runtime.md](12-harness-runtime.md) | Memory lifecycle, replaceable execution environments, goal budgets and information boundaries, with source video timestamps | whoever operates long-running or shared agents |
| `skills/` | Eight rule sets, installable into an agent runtime so the rules apply while the agent works | the team's agents, not the humans |
| `agents/` | Four English-only subagents that route explicit second-opinion requests to isolated, read-only CLI runs | engineers who want a separate review pass through another configured route |
| [monitoring/](monitoring/README.md) | Separate token ledger and coverage report for second-opinion CLI runs | whoever tracks review consumption |
| `INSTALL.md` | How to install the eight rule sets and four second-opinion agents, then confirm they loaded | whoever sets up the client's environment |

## How the pieces fit

The eight rule sets are not eight opinions about the same thing. They govern **different units of
work**, which is why they do not compete and why applying one to another's problem does not help.

| Rule set | Unit it governs | Time horizon |
|---|---|---|
| `earned-length` | one authored artifact: a comment, a response, a report | the moment before it is written or kept |
| `simplicity-ladder` | one change, before it is written | minutes |
| `boundary-dispatch-matrix` | one change that moves execution across a process, queue or service boundary | minutes to hours |
| `cherny-workflow` | one session | hours |
| `execution-state` | one long-horizon run inside a session: what its prompt carries and what its state owns | minutes to hours, tens to hundreds of steps |
| `agentic-factory` | the stream: many loops landing on trunk | weeks |
| `grilling` | a plan, before any of the above starts | one conversation, in rounds |
| `autoresearch` | one experiment inside a measured loop, and the ledger it lands in | minutes per run, a day per rehearsal |

Careful individual changes do not pay down debt accumulated by the stream. A rule from one level
does not fix a problem at another. **Name the level first** is the single most useful habit in the
method.

## Second-opinion agents

The four optional subagents are explicit routes, not automatic reviewers. Use one only when the
user names that route or asks for a second opinion from it. Its output is advisory and does not
replace repository evidence, the oracle, or a human decision boundary.

| Agent | Route | Isolation |
|---|---|---|
| `claude-thinking` | Claude Code CLI | plan mode with read-only file tools |
| `codex-thinking` | Codex CLI | read-only sandbox with isolated user configuration |
| `cursor-thinking` | Cursor Agent CLI | plan mode pinned to an exact model identifier |
| `gemini-thinking` | Antigravity CLI | read-only permission allowlist with pinned model identifiers |

## Running it with a client

1. **Grill the plan.** Before assessing anything, interrogate what the client believes they are
   building and why. `grilling` exists for this and produces the scope of the assessment.
2. **Audit the repository.** Work through `02-audit-checklist.md` inside the codebase. Every answer
   comes from looking, not from asking. `03-worked-example.md` shows what finished looks like.
3. **Produce two outcomes, not one.** A repository level on the existing readiness model, and a
   separate binary decision for one class of change: may it update trunk unattended, under what
   limits. The second is granted to a class of task, never to a repository.
4. **Install the rule sets** so the agents work inside the method rather than beside it.
5. **Set the change-size ceiling from the repository's own p75**, not from a book. Three
   repositories of one team measured p75 of 5, 6 and 12 changed files. One number would have been
   wrong for all three.

## What this kit deliberately does not do

- **It introduces no new maturity scale.** Scoring stays on the AI Agent Readiness model in
  `04-readiness-model.md` (5 levels, 11 pillars). The method tells you what to measure and where the
  gates are; the scale is unchanged. Read that model's Pillar 11 caveat before scoring anything: a
  team that does not run multi-agent workloads scores the pillar honestly and then marks it "Not
  pursued", excluding it from the minimum. Skipping that rule is how the worked example first
  produced three L1 verdicts in a row, which is why the correction is left visible in it.
- **It does not promise autonomy.** The honest output of an assessment is often "this class of
  change may land unattended and nothing else may", and that is a useful answer.
- **It does not paper over what is unknown.** `01-method.md` ends with the questions the primary
  sources do not answer, including how to measure comprehension debt and what to do on a brownfield
  codebase. Those are stated rather than smoothed over, because a client will hit them.

## On names and attribution

Three decisions worth knowing before this goes to a client.

**Cited authors are named.** Where a rule comes from published work by a named person or a public
repository, the author and the source are named. `cherny-workflow` is derived from a published
engineering guide and says so. Removing that attribution would be presenting someone else's work as
ours.

**A competitor's product documentation is cited by class and date, not by name.** Where material
comes from a competitor's product documentation, the file records what was taken, what kind of source
it was and when it was read, and states that the vendor is unnamed by this rule. The provenance stays
checkable and the kit does not carry a competitor's name to a client.

The rule is about competitors, not about every company. Model and platform providers whose published
engineering material this kit draws on are named, as are individual authors: naming the source is
what makes a derived rule checkable, and those providers are not the parties a client is choosing
between when they read this. `10-repo-standard.md` names one such provider for that reason, and
de-identifies a competitor's standards document in the same paragraph.

**Runtime-specific material is isolated.** `INSTALL.md` names runtimes because installation has to
say where files go. `04-readiness-model.md` names them because several pillars are about the
agent-facing surface itself: which context file a runtime reads, which protocols it speaks and
which conventions it follows. `agents/` contains the optional second-opinion adapters.
`skills/autoresearch/SKILL.md` names the upstream repository it is derived from and the runtimes it
was written for. In `skills/execution-state/SKILL.md`, section 8 names the CLI routes it applies the
state discipline to and section 7 names the models the source evaluated; sections 1 to 6 and 9 are
free of runtime names.

`01-method.md`, `02-audit-checklist.md` and `03-worked-example.md` are free of it, so those three can
be handed to a client who uses different tooling and they will still read correctly. `05-intent-layer.md`
through `08-measured-loop.md` are free of it as well. The optional agents can be omitted without
changing the method or the eight rule sets. Section 8 of `skills/execution-state/SKILL.md` is the
only part of a rule set that depends on them.

**Every measured incident in here has been de-identified.** The measurements, dates and failure
mechanics are real and unchanged, because they are the evidence. The repository names, commit
hashes, file paths and product names they came from have been removed. If a client asks for the
underlying artifacts, that is a separate conversation about a reference engagement, not a copy of
this kit.
