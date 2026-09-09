# Build or buy: mapping a platform to local equivalents

A client evaluating an intent-layer platform asks one question: buy it, or build it. This file
answers with a procedure and a filled example rather than an opinion, in the same shape as the rest
of the kit: for every capability, name the local equivalent, what it is built from, and the receipt
that shows it works.

The example names a specific vendor, because a mapping without the vendor's own module names cannot
be checked by the reader. Every row rests on that vendor's published material, read on the dates
stated in the sources section, and any figure that came from somewhere else is labelled where it
appears.

## 1. The procedure

1. **Take the vendor's own module list**, from their documentation rather than their sales page. Where
   the two disagree, record both and treat the difference as a question for them.
2. **For each module write three cells**: the local equivalent, what it would be built from, and the
   receipt that distinguishes working from present.
3. **Mark what the vendor does not document.** Not as absence of capability. As "not documented",
   which is a question, not a verdict.
4. **Separate software from what is not software.** Anything that arrives by signature, channel or
   staffing does not appear in a build column at all.
5. **Decide per module, not per platform.** A platform is rarely all worth buying or all worth
   building, and the row-level answer is the useful one.

## 2. The filled example

Observed from public documentation and product pages, 2026-08-20.

| Vendor module | Local equivalent | Built with | Receipt that it works |
|---|---|---|---|
| Requirements documents | markdown in the repository, front matter with id `REQ-nnn`, acceptance criteria copied verbatim | git, a file template, review through a pull request | the id resolves to a file, and the file resolves to every reference to it |
| Blueprints in three levels, with contracts and decision records | the same three levels as files, decision records numbered, component name equal to the code symbol | git, a naming convention | for a component picked at random the symbol is found in code, and the reverse holds |
| Work orders | a ticket in the tracker already in use, or a `WO-nnn.md` file, with one authoritative carrier | the existing tracker | the task has one authority, every other carrier refuses writes |
| Knowledge graph | a build artifact, not a database: edges derived from ids in files and from commit trailers | a script of 200 to 300 lines emitting JSON plus a broken-edge report | the graph rebuilds from a clean clone in one run, and a broken edge fails the check |
| Bidirectional traceability | commit trailer carrying the requirement id, notes carrying the evidence bundle, the CI run id | git, CI | from a line of code up to the requirement and back down, in one pass, without asking a person |
| Drift detection | scheduled CI job comparing specification hashes against a symbol inventory, plus a reviewer with an explicit rubric | scheduled CI, a red check instead of a notification | break the specification against the code on purpose, the check must go red |
| Tests module, listed on the product page while its documentation page returns 404 | the kit's own layer: the nine landing gates, negative control, size ceiling from the repository p75 | already written in this kit | disable the behaviour, exactly its own tests go red and nothing else does |
| Feedback and themes | signal intake into the tracker, triage by rubric, theme linked to a task | a webhook or a mailbox into the tracker | signal to theme to task to landed SHA, recoverable by identifiers |
| Agent skill plus its run directory | the six installed rule sets plus a run directory `.factory/run/<sha>/` holding plan, checklist, evidence bundle, review log | already installed, the directory is a convention | the bundle reads without the chat, and the run is resumable |
| Model catalogue and per-token billing | subscription or direct API, with model and version pinned | the current working setup | the model version appears in the record of every run |
| Decision records for model calls | append-only JSONL: model version, temperature, token counts, timestamps | git or object storage | the record is immutable and exportable |

Rows two, three, four, five and six correspond to `05-intent-layer.md`. Row seven is
`01-method.md` and `02-audit-checklist.md`. Row nine is the run record in `05-intent-layer.md`
section 2.4. Rows ten and eleven are the decision records in `06-judgement-oracle.md` section 2.6.

## 3. What no local build reproduces

None of these belong in a build column, and a comparison that omits them flatters the build option.

| Not software | Why it cannot be built |
|---|---|
| A signature under responsibility for a production defect | it is a contract, and it needs a counterparty willing to sign one |
| A distribution channel into a regulated buyer | it is a relationship, and it takes years |
| Referenceable customers | they accumulate, and they cannot be produced on demand |
| People available to start delivery next week | it is staffing, and it is the actual product in most managed engagements |

The consequence for the decision: buy when what is wanted is one of these four, build when what is
wanted is the software. Confusing the two produces a platform purchase that leaves the
accountability exactly where it was.

## 4. The trap in reading a vendor

**Absence of documentation is not absence of capability.** In the example above, the row about the
tests module says the documentation page returns 404, and it does not say the vendor cannot run
tests. That distinction is the same one `01-method.md` insists on for evidence types: a command that
failed to run is not a negative answer about its subject.

The correct handling is a question, and the vendor should be asked to demonstrate rather than
describe. Which leads to the next section.

## 5. Five measurements that settle a capability claim

Each one produces a number, none can be satisfied by a slide, and all five run inside a pilot on the
client's own material. This is the part of the file worth keeping when the vendor names change.

| Claim under test | Measurement |
|---|---|
| Drift detection works | a labelled set the client prepares, half aligned and half deliberately misaligned; report precision and recall |
| A requirement change propagates | the client changes one requirement, the vendor produces the affected code locations, compare against ground truth prepared beforehand and count misses and false positives |
| Retrieval understands the codebase | twenty questions about the client's own repository whose answers the client already knows; report the share correct |
| Rules can be extracted from legacy code | a module whose rules the client has already written down; report recall against that list and precision on claimed contradictions |
| The platform adds something over the model | the same input processed twice on the strongest model and once on the cheapest; report the divergence between the three outputs |

The fifth row is the one that decides whether a platform is a platform. If quality collapses on a
cheap model, what was bought is a wrapper over a provider, and the wrapper is the part being priced.

## 6. How to use this file with a client

Fill the table for their candidate, with their module names, in their repository context. Two rules
keep it defensible:

- **Every receipt cell must be executable by the client without the vendor present.** A receipt only
  the vendor can produce is a demonstration, not a receipt.
- **Date every row and name the source.** A vendor's product changes weekly; in the example above the
  observed release cadence was roughly one version per week. A row without a date is a claim about a
  product that may no longer exist in that form.

