# The measured loop, and the rehearsal that must precede autonomy

**Status: mandatory.** No class of change is granted an unattended landing under `01-method.md`
before the team has operated a measured loop of its own and produced its ledger. The rehearsal is
cheap, it takes a day, and it answers a question no audit answers: whether this team can run a loop
whose results survive being read by somebody else.

The reference implementation for the protocol is public: `karpathy/autoresearch`
(github.com/karpathy/autoresearch), observed on 2026-08-21 at default branch `master`, last pushed
2026-03-26. Read the licence note in section 5 before touching the code itself.

## 1. Why a loop from another domain is the reference

The repository automates machine-learning research: an agent edits training code, trains for a fixed
five minutes of wall clock, reads one number, and keeps or discards the change. It is the smallest
complete instance of everything this kit argues about, which is why the protocol transfers even
though the domain does not.

| Kit concept | How the reference implements it |
|---|---|
| Loop | edit, run, evaluate, keep or discard, repeat |
| Harness | one editable file; data preparation, tokenizer, fixed constants and the evaluation function are outside it |
| Oracle | a single number, validation bits per byte, lower is better, computed by code the agent is instructed not to touch |
| Comparable runs | a fixed time budget per run, so two results mean something next to each other |
| Evidence | an append-only ledger, one row per experiment, keyed by the commit |
| Failure kept visible | a crash is a row with a status, not a deletion |
| Simplicity ladder | equal result plus simpler code wins |
| Named boundary | the run states what it tested and what it did not cover |

The operating procedure for running that reference, written as a rule set the agent loads at
runtime, ships with this kit as `skills/autoresearch/SKILL.md`. It carries the target checks, the
ledger format, the integrity constraints and the reporting shape, and it refuses to consume compute
until the checkout, the baseline and the ledger header are verified.

## 2. The protocol, and it is the mandatory part

Eight requirements. Each is falsifiable, so each has a receipt.

### 2.1 A baseline before the first change

**Action.** Run the unchanged code and record its result as the first row of the ledger.

**Receipt.** A baseline row carrying the commit and the metric value.

**Otherwise.** Status is "no baseline". Improvement is not measurable, and every later number is a
value without a reference point.

### 2.2 One decisive metric, with its direction written down

**Action.** Name the one number that decides keep or discard, and the direction of better. Soft
constraints are named separately and do not decide by themselves.

**Receipt.** The metric, its direction, and the list of soft constraints with their thresholds.

**Otherwise.** Status is "decision rule unstated", and keep or discard becomes an opinion formed after
seeing the result.

In the reference the metric is validation bits per byte, chosen because it is independent of
vocabulary size, which keeps architectures comparable. Pick the metric for the same reason: it has to
stay meaningful across the changes you intend to try.

### 2.3 A fixed comparison budget

**Action.** Fix what each run is allowed to consume: wall time, compute, tokens, or dataset. Changing
the budget invalidates the history and starts a new ledger.

**Receipt.** The budget, and the statement that no row in the ledger was produced under a different
one.

**Otherwise.** Status is "runs not comparable". Two numbers produced under different budgets are two
facts about two experiments and not a comparison.

A [persistence budget](12-harness-runtime.md#3-persistence-budget-and-comparison-budget) has a
different purpose: preventing early stopping on an authorised goal. It does not replace the fixed
budget required for comparing experiments.

### 2.4 A declared edit surface, enforced rather than requested

**Action.** Declare exactly what the loop may modify. Everything that produces or validates the
result sits outside that surface: the evaluation function, the data, the fixed constants, the
dependency set.

**Receipt.** The list of paths the loop may write, plus the mechanism that refuses a write outside it.

**Otherwise.** Status is "edit surface unenforced", and the first oracle failure mode from
`01-method.md` section 3 applies in full: the agent authors both the work and the proof.

This is the requirement that most often degrades into a convention. In the reference the constraint
is written as an instruction to the agent, which makes it a request. A request is adequate for a
research loop on a personal machine and is not adequate for anything landing on a shared trunk. Bind
it: a check that the diff touches only declared paths, run where the loop cannot disable it, and the
verdict recorded against the candidate commit.

### 2.5 An append-only ledger keyed by the commit

**Action.** One row per experiment: commit, metric value, the soft-constraint reading, status, and a
one-line description of the hypothesis. Statuses distinguish accepted, rejected, and failed to run.
Never overwrite a row and never delete one.

**Receipt.** The ledger, with its crash rows present.

**Otherwise.** Status is "history unavailable". A ledger with the failures removed reports a success
rate of one hundred percent and is worth nothing to the next person.

The reference uses a five-column tab-separated file and reserves a status for a crash with zeroed
values, so a run that died is visibly a run that died rather than an absence. Copy that property, not
necessarily the format.

### 2.6 The hypothesis is written before the run

**Action.** State what this change tests, in one line, before starting it.

**Receipt.** The description column, populated at the time of the run rather than reconstructed
afterwards.

**Otherwise.** Status is "post hoc explanation". A hypothesis invented after the number is a story
about the number.

### 2.7 The simplicity tiebreak

**Action.** When results are equal within noise, keep the simpler code. Keep a tiny gain only when
its complexity cost is reasonable, and say what the cost is.

**Receipt.** For each kept row where the gain was marginal, the sentence that justifies its
complexity.

**Otherwise.** Status is "accumulating complexity for noise", which is how a loop produces a codebase
nobody wants after two hundred green experiments.

### 2.8 The uncovered conditions, named per run

**Action.** With every accepted result, state which material conditions the experiment did not cover.

**Receipt.** That statement, next to the row or in the run report.

**Otherwise.** Status is "scope of the result unknown", and a result whose scope is unknown will be
generalised by whoever reads it next.

## 3. The rehearsal gate

**Trigger.** A team asks for an unattended landing decision for any class of change, under
`01-method.md` section 5.

**Action.** Before the decision, the team runs a measured loop of its own for one working day. Any
domain: a performance number, a bundle size, a suite runtime, a defect-detection rate on a fixed
corpus. The loop must satisfy the eight requirements of section 2.

**Receipt.** The ledger from that day, containing a baseline row, at least one accepted row, at least
one rejected row, and any crash rows that occurred, plus the declared edit surface and the budget.

**Otherwise.** The autonomy decision is "not yet", and the reason is recorded as "measured loop not
demonstrated". This is not a judgement about the engineers. A team that cannot yet produce a clean
ledger for one day will not produce one for a stream of agent changes on trunk, and the gates in
`01-method.md` all consume exactly this kind of evidence.

Why this gate is worth its cost: every other artifact in this kit can be produced by a careful writer
in an afternoon. A ledger cannot. It is the one deliverable that requires the loop to have actually
run, and the failure modes it exposes are the ones that matter, which is a run that cannot be
reproduced, a result that moved when nobody changed anything, and an oracle that turned out to be
inside the edit surface.

## 4. Instantiating the protocol outside machine learning

The reference domain needs a single NVIDIA GPU and its results are not comparable across hardware,
which the repository states plainly. Most teams applying this kit have no such loop. The protocol
still applies, with these substitutions.

| Reference | On an ordinary software repository |
|---|---|
| validation bits per byte | one decisive number: p95 latency on a fixed scenario, bundle size, suite runtime, defect-detection rate against a fixed corpus, or cost per request |
| five minutes of training | a fixed cap per run: wall time, or a fixed input corpus, or a fixed number of requests |
| only `train.py` is editable | a declared path list, with the benchmark harness, fixtures and thresholds outside it |
| `results.tsv` | any append-only file in the repository, keyed by commit, with the same columns |
| peak video memory as a soft constraint | whatever must not regress: memory, cost, error rate, accessibility checks |
| a crash row | the run that failed to complete, recorded with its cause |

One caution about choosing the decisive number: a metric the loop can improve by damaging something
unmeasured will be improved that way, and the soft constraints in row five are the only thing
standing in front of that. Name them before starting, not after the first surprising result.

## 5. Licence and dependency status, before anyone clones it

Observed on 2026-08-21 through the GitHub API: the repository has no licence file at the root of
`master`, and the API reports its licence field as null. Public visibility is not a grant of rights.

What follows for this kit and for a client engagement:

- **The protocol in section 2 is what is mandatory.** It is a set of requirements, not code, and it
  carries no dependency.
- **Do not vendor, redistribute, or embed the repository's code** in a client deliverable on the basis
  that it is public. Absent a licence, permission to copy has not been given.
- **Reading it is how it should be used.** It is a reference implementation to study, and the
  requirements above are the transferable part.
- If a client wants to run the reference itself, that is their decision to take with their own counsel,
  and the kit neither requires nor recommends it.

This keeps the kit consistent with the position stated in `01-method.md` section 1, that it bundles no
third-party dependency. Section 2 adds a required practice and names a public reference; it adds
nothing to install.

## 6. Additions to the audit checklist

| # | Pillar | Question |
|---|---|---|
| 3.12 | 3 Testing | Does a measured loop exist with a baseline row, one decisive metric and its direction, and a fixed comparison budget? |
| 3.13 | 3 | Is the ledger append-only, keyed by commit, and does it contain failed runs rather than only successful ones? |
| 7.9 | 7 Security and Governance | Is the loop's edit surface declared and enforced by something the loop cannot disable, with the evaluation code outside it? |
| 4.10 | 4 Documentation and Agent Context | Is each experiment's hypothesis recorded before the run rather than reconstructed after it? |
| 6.5 | 6 Debugging and Observability | Can any row in the ledger be reproduced from what the row records? |

## 7. What this file does not settle

- **How many experiments make a trend.** The reference produces many rows quickly because a run costs
  five minutes. On a repository where a run costs an hour, the number of rows needed for a defensible
  conclusion is unmeasured here.
- **Noise.** Section 2.7 says "equal within noise" and this kit does not tell you how to establish the
  noise band for your metric. Measure the same commit several times before trusting a small gain.
- **Whether a research loop transfers to product code at all.** The author of the simplest published
  autonomous loop says he would not run it on an existing codebase, and `01-method.md` section 11
  records brownfield as an open question. The rehearsal gate deliberately does not require the loop to
  run on the production repository, for that reason.

## Sources and attribution

The protocol in section 2 is derived from `karpathy/autoresearch` by Andrej Karpathy, read on
2026-08-21: its README, and the operating rules it states for the agent. The elements taken are the
single decisive metric, the fixed per-run budget, the restriction of the edit surface to one file with
evaluation and data outside it, the append-only ledger keyed by commit with a status for crashes, the
baseline-first rule, and the simplicity tiebreak.

Not from that source, and belonging to this kit: the rehearsal gate in section 3, the requirement that
the edit surface be mechanically enforced rather than requested, the substitution table in section 4,
the licence position in section 5, the audit rows in section 6, and the open questions in section 7.
