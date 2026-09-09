# The intent layer

The rest of this kit starts at the repository. `01-method.md` states that intent and architecture stay
with the human, and then says nothing about the artifact that carries them. This file supplies that
artifact standard, the edges between artifacts, and the checks that keep the edges honest.

It introduces **no new maturity scale** and **no new gate**. Scoring stays on the eleven pillars in
`04-readiness-model.md`; the landing decision stays on the nine gates in `01-method.md`.

## 1. What this layer is for, and what it cannot do

Read this section before the rest, because the most common way to waste this file is to mistake it
for an oracle.

| | |
|---|---|
| It feeds | **G1 Scope**: a task has a checkable completion condition written down before work starts |
| It produces | **G6 Evidence**: a diff, checks and logs that a reader can trace to a stated intent |
| It does **not** grant | **G4 Oracle**. Every artifact here is authored by whoever does the work, so it is fakeable by construction |
| Pillars it moves | 4 Documentation and Agent Context, 8 Task Discovery, 9 Product and Experimentation |

An identifier pasted into a commit message proves that somebody pasted an identifier. Treat this
layer as the input to a human gate and as the substrate for audit, never as proof of correctness.
Where correctness matters, the oracle rules in `01-method.md` section 3 still decide, and for tasks
whose correctness is a judgement, `06-judgement-oracle.md` gives the pattern.

The one thing this layer does that no oracle does: it makes the question "what was this change for"
answerable a year later without asking a person who may have left.

## 2. Four artifacts

### 2.1 The requirement

**Trigger.** Work is requested that changes observable behaviour.

**Action.** Write a file carrying a stable identifier, the outcome in the language of whoever asked
for it, the acceptance criteria, and the boundary. Implementation belongs in the architecture
document, not here.

Required fields: `id` (stable, never reused), title, the outcome and who wants it, acceptance
criteria as a numbered list, out of scope as a list, owner, review date.

**Receipt.** The identifier resolves to exactly one file, and the file resolves to every reference to
it in the repository through one search.

**Otherwise.** Status is "intent not recorded". The work may proceed under an explicit human owner,
and it does not qualify for an unattended landing, because G1 has nothing to check against.

One rule about acceptance criteria that is worth more than the rest of this section: **criteria are
copied into the work unit without rewording, and they carry their identifiers with them.** A reworded
criterion is a second requirement nobody approved.

### 2.2 The architecture document

**Trigger.** A change adds a deployable unit, a shared capability, or a feature that composes them.

**Action.** Write at the level that matches the change, and only at that level. Three levels:

| Level | Covers | Written when |
|---|---|---|
| Deployable unit | one independently deployed thing: service, web application, worker, store. Technology, runtime characteristics, entry points, cross-cutting concerns | the unit is introduced or its boundary moves |
| Capability | one reusable capability that several features compose, usually crossing unit boundaries | the capability is introduced or its contract changes |
| Feature | how a feature composes existing capabilities, plus the components that exist only for it | per feature, kept short by composing rather than restating |

Every level carries two sections that are not optional:

- **Contracts.** The invariants and reliability semantics somebody else depends on: idempotency,
  ordering, consistency, retry behaviour, what is published and consumed. This section is what makes
  the document usable by an agent, because it is the part that cannot be inferred from the code in
  one read.
- **Decision records.** Numbered, three paragraphs each: why the decision was needed, what was
  chosen, what it costs. A decision without its consequences paragraph is a preference.

**Receipt.** For a component picked at random from the document, the corresponding symbol is found
in the code, and for a symbol picked at random from the code on that path, the document names it.
Run the check in both directions; one direction passes trivially.

**Otherwise.** Status is "architecture not grounded". The document may be useful prose, and it is not
evidence, because nothing ties it to what runs.

Naming rule: a component in the document carries the name of the code symbol. When the two names
diverge, the cross-layer vocabulary gate in `01-method.md` section 8 applies, and the divergence is
either a classified boundary mapping or a defect.

### 2.3 The work unit

**Trigger.** A requirement is ready to be executed by a person or an agent.

**Action.** One authoritative carrier per unit of work. Copy the applicable acceptance criteria
verbatim with their identifiers, name the requirement and the architecture documents it rests on,
state what is out of scope, and state the completion condition in a form somebody else can check.

**Receipt.** The unit names its requirement identifier, its completion condition is checkable without
asking the author, and no second carrier for the same work exists in another system.

**Otherwise.** Status is "work not scoped". A unit whose completion condition is an opinion cannot
pass G1, whatever its maturity level.

### 2.4 The run record

**Trigger.** An agent or a person starts work on a unit.

**Action.** Create a run directory in the repository holding the plan, the checklist, the evidence
bundle and the review log. The evidence bundle carries the base SHA, the candidate SHA, the commands
that were run, their exit codes, tool versions, the suite manifest and the run identifiers.

**Receipt.** The bundle reads without the chat that produced it, and a second person can rerun the
same commands from it.

**Otherwise.** Status is "evidence not recorded", which is a G6 failure and blocks an unattended
landing on its own.

## 3. The edges, and why the graph is a build artifact

The value of the four artifacts is not in the documents. It is in the edges: requirement to
architecture to work unit to landed change to production signal, traversable in both directions.

**Do not build a database for this.** Every edge already exists in a place that is append-only and
that nobody has to remember to update separately:

| Edge | Where it lives |
|---|---|
| work unit to requirement | the requirement identifier inside the work unit |
| landed change to requirement | a trailer in the commit message |
| landed change to evidence | notes attached to the commit, or the run directory keyed by candidate SHA |
| landed change to checks | the run identifier inside the evidence bundle |
| production signal to work unit | the signal identifier inside the work unit that answers it |

**Action.** Write one builder that walks these places and emits the graph, plus a report of edges
that point at nothing. Wire the report into the checks that run on every change.

**Receipt.** The graph rebuilds from a clean clone in a single run, with no state carried over, and a
broken edge fails the check rather than printing a warning.

**Otherwise.** Status is "traceability not established". A graph maintained by hand describes the day
somebody last maintained it.

Why a build artifact rather than a store: a store has to be kept in sync with the repository, which
adds a second thing that can be stale, and staleness in the traceability layer is invisible until
somebody needs the trace. A derived graph cannot be stale; it can only be broken, and broken is
loud.

## 4. The hotfix path, counted rather than forbidden

**Trigger.** An urgent change has to land before its artifacts can be written.

The observed failure mode of every traceability scheme is not refusal. It is the first justified
bypass becoming permanent in silence: the urgent change goes in without a trailer, nothing breaks,
and the exception spreads until the checks are noise and somebody makes them non-blocking.

**Action.** Name the exemption, do not prohibit it. The bypass carries an explicit marker, the
counter for bypasses is visible where the team looks anyway, and each one carries an owner and a date
by which its artifacts are backfilled.

**Receipt.** The count of exempt landings for the period, with the backfill state of each.

**Otherwise.** Status is "exemption path unknown", which in practice means the bypass exists and is
not measured.

## 5. The coherence sensor

A sensor compares the artifacts against the code and raises a signal when they diverge.

**The rule that decides whether it is worth anything:** a notification that a person reads is a human
gate, and this kit already says so in `02-audit-checklist.md`, note on 3.3. A sensor becomes a gate
only when its verdict can refuse a ref.

**Order of work, and it does not compress:**

1. Run in observe mode. It writes its verdicts and blocks nothing.
2. Build a labelled set from the repository's own history: changes known to be aligned with their
   stated intent, and changes deliberately misaligned. Both halves are required; a set of only bad
   examples measures nothing.
3. Measure precision and recall against that set. Write the numbers down next to the date and the
   commit the sensor ran at.
4. Name the threshold at which it becomes blocking, and for which paths.
5. Give it a negative control of its own: rewrite a specification so it contradicts the code, and the
   sensor must fire; leave an aligned change alone, and it must not.

**Receipt.** Precision and recall on a named labelled set, plus the negative control result, both
bound to a SHA.

**Otherwise.** Status is "sensor not calibrated". It may run in observe mode indefinitely, and it may
not block, and its output may not be described as a check.

**What the sensor does not do.** It does not propagate a change from a requirement into code. Nobody
has that, including the products that advertise the sentence; what they ship is a sensor plus a
guided workflow with a human in it. Promising propagation is the fastest way to lose the credibility
of the whole layer.

## 6. Backlog authority

**Trigger.** More than one system can hold a unit of work.

**Action.** Name one authoritative carrier. Every other place becomes read-only, and the closure is
mechanical rather than social: remove the create permission, or route creation into the authority.

**Receipt.** For a unit picked at random there is exactly one carrier that can change its state, and
the others refuse writes.

**Otherwise.** Status is "authority not established". Two authorities is a permanent reconciliation
task and it eventually produces two different answers to "is this done".

## 7. Additions to the audit checklist

These rows extend `02-audit-checklist.md`. They are answered by looking at the repository, in the
same way as the rows already there.

| # | Pillar | Question |
|---|---|---|
| 4.5 | 4 Documentation and Agent Context | Does a landed change resolve to a stated intent through a mechanical trace, without asking a person? |
| 4.6 | 4 | Does the traceability graph rebuild from a clean clone, and does a broken edge fail a check? |
| 4.7 | 4 | For a component picked at random from the architecture document, is the code symbol found, and in the other direction as well? |
| 4.8 | 4 | Are exempt landings counted, with an owner and a backfill date each, rather than prohibited on paper? |
| 8.4 | 8 Task Discovery | Is there exactly one authoritative carrier per unit of work, with the others refusing writes? |
| 8.5 | 8 | Does a unit of work state a completion condition another person can check without asking its author? |
| 9.4 | 9 Product and Experimentation | Does a production signal resolve to the unit of work that answered it, by identifier? |
| 3.7 | 3 Testing | If a coherence sensor exists, are its precision and recall measured on a labelled set, and is its blocking threshold named? |

Score them inside their pillars under the existing rule: the highest level at which at least 80% of
items pass, and the repository level is the minimum across pillars.

## 8. What this layer does not do

State these to a client at the start rather than when they are discovered.

- **It is not an oracle.** Section 1. Everything here is authored by the party being checked.
- **It does not measure comprehension debt.** The gap between code written and code understood is
  untouched by traceability, and a well documented change can still be a change nobody read.
- **It does not survive without an owner.** The artifacts decay at the speed of the first unmeasured
  exemption. Section 4 is the whole defence, and it is procedural.
- **It does not make architecture cheap.** The document is written by somebody who knows the system.
  An agent drafts it; the naming, the contracts and the consequences paragraphs are read by a human
  before the document is trusted, because a plausible contracts section is worse than none.

## Sources and attribution

The three-level document schema with contract and decision sections, the practice of copying
acceptance criteria verbatim with their identifiers into the unit of work, the framing of a
requirement-to-code traceability graph as the substrate of the whole thing, and coherence drift as a
background sensor: these are taken from published commercial documentation for a software factory
product, specifically its requirements, blueprint and work-order writing guides and its module
documentation, read on 2026-08-20. That vendor is not named here, per the attribution rule in
`README.md`. The kit adopts the schema and rejects the accompanying claim that a requirement change
propagates into code, for the reason given in section 5.

The underlying practices are older than that documentation and are standard in requirements
engineering: layered specification, acceptance criteria carried by identifier into the unit of work,
and requirement-to-implementation traceability. What the documentation contributed is one worked
assembly of them.

The deployable-unit and capability levels correspond to the container and component levels of the C4
model by Simon Brown. The decision record format is Michael Nygard's, in its usual short form.

Not from those sources, and belonging to this kit: the gate and pillar mapping in section 1, the
insistence that the graph is a derived artifact rather than a store, the counted exemption path in
section 4, the calibration order and the negative control for the sensor in section 5, and the audit
rows in section 7.
