# The oracle for judgement tasks

`01-method.md` section 3 requires an oracle that is cheap, frequent and unfakeable at once, and every
example it gives is a typed gate: a property test, an invariant, a contract. That leaves a class of
work with no oracle at all, and it is the class agents are increasingly given: the task whose
correctness is a judgement rather than a comparison.

This file gives the pattern for that class, its price, and the limits that stay after it is built.
It adds no scale and no gate. It is what makes G4 answerable where a typed gate does not exist.

## 1. When this applies, and when it does not

**Applies when** the output is a document, a summary, an extraction, a classification, a rewrite, a
diagnosis, or a recommendation, and two qualified people could disagree about whether a given output
is correct.

**Does not apply when** a typed gate is available. Building a judge for something a schema, a parser
or a property test can decide is a way to make a cheap check expensive and weaker. Check first
whether the criterion can be made deterministic; the ladder in `skills/simplicity-ladder/SKILL.md`
applies to oracles as much as to features.

**The four ways an oracle silently stops being one apply here without change**, and the first one
bites hardest: a judge whose prompt, rubric and dataset are edited by the same party that produces
the candidate is not a check. Put the rubric and the dataset where the producing side cannot alter
them, and bind each verdict to the candidate identity.

## 2. The pattern, six parts

None of the six is optional, because each one closes a specific way the measurement flatters the
system.

### 2.1 A reference set with adjudicated disagreement

**Action.** Assemble items produced before the system existed, or held out from it, and have
qualified people score them against the rubrics. Where two scorers disagree, adjudicate the item and
record the resolution rather than averaging it.

**Receipt.** The set, its size, who scored it, the date, and the list of adjudicated items with their
resolutions.

**Otherwise.** Status is "no reference". A judge with no reference set is an opinion generator with a
numeric output format.

Averaging away a disagreement destroys the most informative item in the set: the one where the
rubric was ambiguous.

### 2.2 Two rubrics, not one

**Action.** Run two independent rubrics over the same output, each with its own scope. One covers
completeness and evidence: is everything required present, is every claim supported. The other covers
fitness for its destination: tone, form, and whatever the receiving side will refuse it for.

**Receipt.** Both rubrics, their criteria, and per-item scores from each.

**Otherwise.** Status is "single-rubric measurement", which is blind exactly outside its own scope,
and the gap does not announce itself.

### 2.3 Score before a human edits it

**Action.** Snapshot the output at generation, immutably, and score that snapshot. Track human edits
separately as a second measurement.

**Receipt.** Two numbers per item: pre-edit and post-edit, plus the edit distance between them.

**Otherwise.** Status is "measurement contaminated". A skilled reviewer rescues weak output, the
final artifact looks good, and nothing in the record distinguishes a strong generator from a strong
reviewer. This single rule is the difference between measuring the system and measuring the team
around it.

### 2.4 A metric chosen from the cost asymmetry

**Action.** Before measuring, write down which error costs more: the miss or the extra. Then pick the
metric that weights it. Where a miss is the expensive error, weight recall above precision and say by
how much. Where an extra costs more, do the reverse.

**Receipt.** The stated asymmetry, the metric formula, and the reason in one sentence.

**Otherwise.** Status is "metric unaligned with stakes". A balanced score optimises for neither of
the two errors the work actually has.

### 2.5 An owner, a cadence, and a review date

This part closes an open question this kit has carried since `01-method.md` section 11: who owns the
oracle and how its staleness is caught.

**Action.** Name a person. Set the interval at which the judge is re-scored against the reference set
and the rubrics are revisited. Put the next date in the artifact.

**Receipt.** Owner, interval, date of last calibration, date of next, and the drift observed at the
last one.

**Otherwise.** Status is "oracle unowned", and it should be treated as expired rather than as
working, because a judge drifts silently while continuing to emit numbers.

The cost of this part is real and it is people: pulling qualified reviewers off delivery work for
some days each cycle. Say the number out loud when proposing the pattern. A cadence nobody funds is
not a cadence.

### 2.6 Decision records

**Action.** For every scored run, append a record: model identity and version, sampling parameters,
timestamp, token counts, input hash, rubric version, dataset version, and the verdict. Append-only,
outside the reach of the process being judged.

**Receipt.** A record retrievable by candidate identity, immutable, exportable.

**Otherwise.** Status is "verdict unattributable". Without the model version and the rubric version,
a change in scores cannot be told apart from a change in the scorer.

## 3. The negative control for a judge

`02-audit-checklist.md` line 3.5 requires a negative control for critical modules. A judge needs one
of its own, and it is a different test.

**Action.** Three probes, all bound to a dataset version:

1. **Known-bad injection.** Feed items with a defect deliberately introduced in the dimension the
   rubric claims to cover. The judge must reject them, and must name the dimension.
2. **Known-good control.** Feed items the reference set already accepted. The judge must pass them.
3. **Self-drift.** Re-score the reference set at each calibration and compare against the previous
   scores of the same items. Movement without a rubric change is judge drift.

**Receipt.** Rejection rate on known-bad, pass rate on known-good, and the self-drift figure with
dates.

**Otherwise.** Status is "judge unverified", and its output may not be used to grant autonomy. It may
still be used as a human-facing signal, labelled as such.

## 4. What this pattern still does not solve

Say these before a client discovers them.

- **Calibration does not transfer between clients.** A reference set is built from one organisation's
  material and cannot be shared into another. Each engagement pays for its own. No published method
  removes this, and the vendor material this pattern is drawn from states the same limitation.
- **A judge carries known biases.** Order of presentation and phrasing of the rubric move scores.
  Calibration reduces the drift and does not remove the bias.
- **Small samples describe a direction, not a level.** A trajectory over a couple of dozen items is
  worth having and is not a claim about the population, and it should be reported as indicative.
- **It does not make the task autonomous.** A judge that passes section 3 is evidence for G4 on a
  named class of task, under the back-pressure rule: as much autonomy as can be verified cheaply and
  reliably, and no more.

## 5. Additions to the audit checklist

| # | Pillar | Question |
|---|---|---|
| 3.8 | 3 Testing | For each task class whose correctness is a judgement, is there a reference set with adjudicated disagreements, and where does it live relative to the producing party? |
| 3.9 | 3 | Are outputs scored before human editing, with the pre-edit snapshot immutable? |
| 3.10 | 3 | Does the judge have a negative control: known-bad rejected, known-good passed, self-drift measured? |
| 3.11 | 3 | Is the metric chosen from a written statement of which error costs more? |
| 7.4 | 7 Security and Governance | Does each judgement oracle have a named owner, a calibration interval, and a next review date that has not passed? |
| 6.4 | 6 Debugging and Observability | Is there an append-only record per scored run carrying model version, parameters, rubric version and dataset version? |

## 6. The smallest version worth building

For a team that has never done this, the order that gets to a usable oracle fastest:

1. Pick one task class where a miss is expensive. One, not three.
2. Collect twenty to fifty items, scored by two qualified people, disagreements adjudicated.
3. Write both rubrics as checklists of binary criteria before automating anything.
4. Score the next month of output pre-edit by hand against those rubrics. This is the baseline, and it
   is worth having even if no judge is ever automated.
5. Only then automate the judge, and calibrate it against the set from step 2.
6. Put the owner, the interval and the next date in the file on the day the judge starts running.

Steps 1 to 4 produce most of the value, and they are the steps teams skip in order to get to step 5.

## Sources and attribution

The bundled pattern in section 2, that is the reference set with adjudicated disagreement, two
independent rubrics rather than one, scoring an immutable pre-edit snapshot, a recall-weighted metric
chosen from the cost asymmetry, periodic recalibration of the judge against the reference set, and
append-only decision records carrying model version and sampling parameters, is taken from a
published commercial account of an evaluation framework built for AI-assisted document authoring in a
regulated domain, read on 2026-08-20. That vendor is not named here, per the attribution rule in
`README.md`. The limitations in section 4 are stated in that same account by its authors, and they
are reproduced here rather than dropped.

The component practices predate that account and are common in evaluation work: held-out reference
data, inter-rater adjudication, a model judging against a rubric, and cost-weighted metrics. What is
taken is the combination and the ordering.

Not from that source, and belonging to this kit: the applicability boundary in section 1 and the
instruction to prefer a deterministic check, the negative control for a judge in section 3, the audit
rows in section 5, the smallest-version order in section 6, and the placement of the whole file as
evidence for G4 under the existing back-pressure rule.
