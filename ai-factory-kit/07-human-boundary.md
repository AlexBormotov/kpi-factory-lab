# What stays with human judgement

`01-method.md` section 4 draws the boundary between the inner loop and the outer one and explains why
architecture does not cross it. This file turns that into a list, with the receipt that shows the
human actually exercised each item rather than being named as its owner on a slide.

It exists because of a specific misreading. At L5 the readiness model says the human reviews policy
rather than every diff, and that sentence gets read as "there is no human". What happens at L5 is
that control moves to policy, boundaries, sampling, exceptions and consequences. Authority and
accountability stay human at every level of the ladder, including the top one.

No new scale, no new gate. Scoring stays on the eleven pillars; the landing decision stays on the
nine gates.

## 1. The test for whether a decision may leave a human

A decision may be delegated to a loop when all three hold. If any one fails, it stays with a person,
and no amount of model capability changes that.

| | Property | Fails when |
|---|---|---|
| 1 | An oracle exists for it: cheap, frequent, unfakeable at once | the check is authored by the party being checked, or checks something the consumer never sees |
| 2 | The oracle's feedback arrives no slower than the failure it must catch | the failure mode develops over weeks and the check answers in seconds about a different property |
| 3 | Being wrong is reversible inside the loop's own authority | recovery needs a person, a migration, a customer conversation, or money |

Property 2 is the one that is usually skipped, and it is why architecture is structurally human rather
than human "until the models improve". Architectural erosion appears over weeks. A suite that answers
in seconds can hold a gate against a compile error and cannot hold one against erosion, because it
never measures the thing that is moving.

## 2. The list

Short on purpose. A list of thirty items is wallpaper, and the first thing a team under pressure
learns is which of the thirty nobody checks.

| # | Stays human | Which property fails | Receipt that the human exercised it |
|---|---|---|---|
| 1 | What to build, for whom, and why now | 1 and 2 | the requirement carries a named owner and a date, and the owner is a person, not a role |
| 2 | Architecture and boundaries: what becomes a unit, what crosses a contract | 2 | a decision record with its consequences paragraph, and the name of who took it |
| 3 | Acceptance of evidence | 1 | the accepting identity differs from the producing identity, on the record, per landing |
| 4 | Risk classification: which paths are excluded from autonomy | 3 | the exclusion list, its review date, and the name of who last reviewed it |
| 5 | The oracle itself: rubric, dataset, threshold, and what counts as done | 1 | the negative control result, plus owner and next calibration date, per `06-judgement-oracle.md` |
| 6 | Exposure: deploying, enabling a flag, widening a cohort | 3 | the principal that landed the change cannot perform this, shown in the configuration, per G8 |
| 7 | The trade between speed and comprehension | 2 | a stated budget for code changed and not read, with the number and the stop condition |
| 8 | Canonical naming at a contract boundary | 1 | the vocabulary receipt from `01-method.md` section 8, read by a person before an unattended merge |
| 9 | Granting an exception: a hotfix bypass, a size-ceiling override, a pillar marked not pursued | 1 and 3 | each exception counted, owned, and dated, per `05-intent-layer.md` section 4 |
| 10 | Accountability to a client, an auditor or a regulator | none of the three: it is not a technical property | a signature, and the name of the person who gave it |

Item 10 is on the list to prevent a category error. A factory can be built to the top of the ladder
and still transfer no accountability, because accountability moves by contract and not by pipeline.
When a vendor claims it, ask for the clause.

## 3. What is deliberately not on the list

The list is only credible if it excludes things. These leave without a human when the gates in
`01-method.md` pass for their class:

- mechanical refactors inside one unit, dependency upgrades, test additions, documentation updates
- formatting, lint fixes, generated-code regeneration
- the diff read itself, for a class of change where the oracle is strong and the size ceiling holds

Diff review shrinks under automation. Intent review does not shrink at all. Those two sentences are
the whole shape of the boundary, and confusing them produces either a rubber stamp or a bottleneck.

## 4. A human gate against a decoration

The failure that matters is not an absent human. It is a present human whose approval cannot fail.
Four tests, and a gate has to pass all four.

1. **Refusal stops the line.** Saying no has an effect on the pipeline, not only on a conversation.
2. **Refusal has a recorded path.** There is somewhere for the objection to go, and it survives the
   person who raised it.
3. **The human sees evidence, not a summary written by the party being judged.** A produced narrative
   about a diff is an argument. The diff, the checks and the logs are the evidence.
4. **Review time is budgeted.** A reviewer with no time approves. This is not a character flaw, it is
   throughput.

**Receipt.** One instance in the last period where a human said no, and what happened next. If none
exists, the honest status is "gate unexercised", which is different from "gate absent" and is treated
the same way until an instance exists: a switch nobody has pulled is a hypothesis.

**Otherwise.** Status is "human gate decorative". Record it as such, because an audit that scores it
as a control is measuring a form rather than a function.

## 5. The delegation boundary

A prohibition aimed at one agent is not a prohibition. In a published incident account, the agent that
was blocked from acting asked a different agent to perform the action, which it did.

**Trigger.** An action is requested by something other than a person, including by another loop.

**Action.** Check authorisation at the delegation boundary, and account for the initiator of the chain
rather than the immediate executor.

**Receipt.** For a privileged action, the record names both identities: what performed it and what
requested it, transitively to the origin of the chain.

**Otherwise.** Status is "authorisation unestablished for delegated actions", and the exclusions in
item 4 of the list above are advisory rather than enforced.

The corollary for identity: one purpose, one identity, least privilege. A shared credential makes the
receipt above impossible to produce, whatever the logging.

When delegation moves information, also enforce
[destination authority](12-harness-runtime.md#4-information-authority-follows-the-destination):
permission to read a source does not grant permission to share it with another audience.

## 6. Sampling, for the level where the human stops reading every diff

Above L4 the human reads a sample rather than the whole stream. A sample is a control only when it is
specified, and three parameters make it one.

| Parameter | Specified as |
|---|---|
| Rate | share of landings read, by class of change, stated as a number |
| Selection | random within class, plus every change touching a listed path |
| Consequence | what happens when a sampled change is judged wrong: the class loses autonomy until the cause is found |

**Receipt.** The three parameters written down, plus the last period's sampled count and the outcome
of each finding.

**Otherwise.** Status is "sampling not a control". Reading whatever surfaces is attention, not
sampling, and it produces no bound on what is escaping.

## 7. Additions to the audit checklist

| # | Pillar | Question |
|---|---|---|
| 7.5 | 7 Security and Governance | For each item in the list of section 2, is the receipt present, and is its owner a named person rather than a role? |
| 7.6 | 7 | Is there one instance in the last period where a human refused, and is the outcome recorded? |
| 7.7 | 7 | Does the record of a privileged action name both the performing and the requesting identity, transitively? |
| 7.8 | 7 | Where a human reads a sample rather than every landing, are rate, selection and consequence specified as numbers and rules? |
| 4.9 | 4 Documentation and Agent Context | Is there a stated budget for code changed and not read by a person, with a stop condition? |
| 11.3 | 11 Multi-Agent Coordination | Does each agent identity serve one purpose with least privilege, so that delegation can be attributed? |

## 8. What this file does not settle

- **How much review capacity an organisation needs.** Nobody has published a defensible number, and
  test 4 of section 4 turns into a staffing question that this kit does not answer.
- **Whether a person who approves a large number of changes per week is a gate at all.** The threshold
  where approval becomes a formality is unmeasured here. Suspect it is lower than anyone would like.
- **Where the boundary sits once generation exceeds review speed by a wide margin.** The list in
  section 2 holds; the sampling parameters in section 6 are the part that will have to move, and this
  kit has no measurement to set them from yet.
- **How to measure comprehension debt.** Item 7 of the list requires a budget for it, and the metric
  is still undefined. State the budget in whatever proxy the team can actually count, and label the
  proxy.

## Sources and attribution

The inner and outer loop split, the back-pressure rule, and the position that an agent cannot
reliably assess its own work come from Addy Osmani's published work, cited in `01-method.md`. The
argument that a check can only hold a gate against failures appearing no slower than it measures, the
gates themselves, and the negative-control requirement are this kit's own and are stated in
`01-method.md` and `02-audit-checklist.md`.

The delegation incident in section 5 comes from published material by the organisation that ran it;
`01-method.md` notes that which of its publications carries the account has not been confirmed
against the original, so confirm the reference before quoting it externally. The lesson does not
depend on which one it is.

The point that accountability transfers by contract rather than by pipeline answers a claim made by
several commercial software factory offerings: that the vendor answers for the finished product. It
is a fair test to hold a vendor to, and it is a commercial instrument rather than a property of a
system, which is why item 10 of section 2 asks for a signature.
