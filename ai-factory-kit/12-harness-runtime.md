# Harness runtime: memory, execution, budgets and information boundaries

Four controls for long-running or shared agent systems. Apply each where its trigger holds;
they extend G5 and G6 and the existing pillars, without adding a maturity level or a landing gate.

Source: [Why The Harness Matters More Than The Model | YC Paper Club](https://www.youtube.com/watch?v=n9xKblqyQ28),
published 7 September 2026. The observations attributed below come from the speakers' account;
the action, receipt and failure rules are this kit's operational requirements.

## 1. A hybrid memory lifecycle

**Trigger.** A task needs earlier observations whose relevance was unknown at arrival, persistent
subagents, or state whose schema must be discovered during the run.

**Action.** Use the hybrid option identified in
[execution-state, section 4](skills/execution-state/SKILL.md#4-where-it-does-not-hold).
Separate active prompt content, live working state and durable storage. Keep an authorised,
retrievable record of observations outside the prompt; retrieve relevant portions by identifier.
Set ceilings for prompt size, live memory and retained storage, with a stop condition if cleanup
cannot keep them within limits. Give each retained item an owner, access scope, version and
retention rule. Retention follows the data policy, including deletion requirements; audit
completeness is defined within that policy.

Checkpoint before evicting live state that a later step needs. Give persistent subagents explicit
running, idle, offloaded and terminal states, with bounded idle retention. Resume by stable identity,
revalidate observations that may have changed, and resolve concurrent updates through a declared
version/conflict policy. An unavailable checkpoint is an explicit recovery failure.

**Receipt.** An isolated run recovers an earlier observation after prompt eviction, resumes an
offloaded subagent, and rejects a stale concurrent write. Record prompt size, live memory and
retained storage across the run. Delete a required checkpoint in the fixture: recovery must report
the missing state rather than fabricate continuity.

**Otherwise.** Status is "hybrid memory lifecycle unverified"; do not claim resumability or bounded
resource use. The fixed-schema results in `execution-state` do not establish either for this hybrid.

## 2. Execution environments as replaceable resources

**Trigger.** An authorised task must survive replacement of its execution environment or needs to
select among environments with different capabilities.

**Action.** Keep task identity, checkpoints, pending operations and evidence outside the replaceable
environment. Select resources within an approved capability, data-location and cost policy.
Changing machines or models does not widen authority or bypass a denied action.

Use the [Boundary/Dispatch Matrix](skills/boundary-dispatch-matrix/SKILL.md) for every dispatch path:
carry identity, deadline, cancellation, operation IDs and resource leases explicitly. Reacquire
leases at the destination. Reconcile pending external actions before replay so that replacing a
worker does not repeat a payment, publication or other side effect. The controller records the
chosen environment and runtime version and can stop the task from outside that environment.

**Receipt.** In isolation, replace the execution environment during a pending operation. The same
task resumes from durable state, reconciles the operation without duplicating its effect and obeys
cancellation. A target outside the approved policy is refused. Removing the durable checkpoint
produces an explicit recovery failure.

**Otherwise.** Status is "environment replacement unverified"; an environment change requires
manual reconciliation before work resumes.

## 3. Persistence budget and comparison budget

**Trigger.** An explicitly authorised long-running task needs protection against premature stopping.

**Action.** Record the goal, completion evidence, an optional minimum effort before an unsuccessful
run may give up, and a hard maximum spend or deadline enforced outside the model. Completion,
user cancellation, denied authority, a safety boundary or a verified blocker can stop it earlier.
Record the reason and the remaining work; a minimum effort never requires spending after success.
Count work across child agents and environment replacements against the same budget.

Keep this policy separate from the
[fixed comparison budget](08-measured-loop.md#23-a-fixed-comparison-budget).
For a quality-versus-budget study, compare candidates within each fixed budget and record several
budget points separately. A longer run may reveal additional capability; it does not make a cheaper
run an equal-cost comparison. A budget exhausted with unmet criteria is an incomplete task.

**Receipt.** An isolated run continues after a premature final answer while the goal is unmet and
authorised work remains. Separate cases demonstrate stopping at verified completion, cancellation,
a verified blocker and the hard cap. The parent and children share one usage ledger.

**Otherwise.** Status is "persistence budget unenforced"; do not describe repeated prompting as a
bounded autonomous run.

## 4. Information authority follows the destination

**Trigger.** Information moves between users, agents, projects, private sessions, shared channels
or model providers, including through summaries, memories and generated artifacts.

**Action.** Check both source access and the destination's right to receive the information.
Bind retrieval to the current principal and audience; recheck before publication or delegation.
Keep source identifiers and access restrictions with derived content until an authorised policy
permits release. Changing wording or passing through another agent does not remove restrictions.
If a destination includes unauthorised recipients, exclude the protected information or obtain
the required release authority before sending it. Do not rely on a prompt to enforce this boundary.

This extends [the delegation boundary](07-human-boundary.md#5-the-delegation-boundary): attribution
establishes who requested an action; it does not establish who may receive its data.

**Receipt.** Synthetic restricted information is readable in an authorised private context and
blocked in a shared context, including through a summary and a child agent. Revoking access also
blocks reuse from cached memory. Record source, destination, principals, policy version and verdict
without copying protected content into the log.

**Otherwise.** Status is "information-sharing authority unestablished"; do not move the information
into the proposed destination.

## 5. Audit questions

Record applicability and the corresponding section's receipt for each row. An unused runtime
pattern creates no requirement to adopt it; applicable controls feed the existing gates.

| Pillar | Question |
|---|---|
| 4 Documentation and Agent Context | Can retained observations and offloaded work be recovered within the memory and access policy? |
| 5 Development Environment | Can a task survive environment replacement without losing state or repeating external effects? |
| 6 Debugging and Observability | Does the usage ledger include child work and enforce the goal's stop conditions? |
| 7 Security and Governance | Are destination permissions enforced for original and derived information? |

## 6. Source observations and boundaries

Read through the original English automatic captions on 7 September 2026; the linked times locate
the source passages. These reports are not local measurements of a kit implementation.

- Seth Karten describes layered context, live-state cleanup and persistent subagent resumption:
  [21:30](https://www.youtube.com/watch?v=n9xKblqyQ28&t=1290),
  [23:42](https://www.youtube.com/watch?v=n9xKblqyQ28&t=1422),
  [26:08](https://www.youtube.com/watch?v=n9xKblqyQ28&t=1568).
- The QM presenters describe moving conversation state outside execution sandboxes and selecting resources:
  [52:06](https://www.youtube.com/watch?v=n9xKblqyQ28&t=3126),
  [55:22](https://www.youtube.com/watch?v=n9xKblqyQ28&t=3322).
- The QM presenters describe goal budgets to counter early stopping; Karten discusses performance at increasing
  expenditure: [57:34](https://www.youtube.com/watch?v=n9xKblqyQ28&t=3454),
  [29:12](https://www.youtube.com/watch?v=n9xKblqyQ28&t=1752).
- The QM presenters describe privileged information leaking across social contexts and the need for
  fine-grained permissions: [58:50](https://www.youtube.com/watch?v=n9xKblqyQ28&t=3530).

Two passages reinforce existing controls. Karten reports that his first near-perfect benchmark run
was cheating and needed proper sandboxing
([31:08](https://www.youtube.com/watch?v=n9xKblqyQ28&t=1868)); this illustrates the isolation concern
in G4/G5, without identifying a specific exploit. The QM presenters report mixed results from automated fixes
with a model judge and continued need for human involvement
([53:23](https://www.youtube.com/watch?v=n9xKblqyQ28&t=3203)).
Apply the existing [harness regression rules](10-repo-standard.md#evals-the-harness-needs-its-own-regression-suite)
to changes in prompts, skills or runtime behaviour. Benchmark gains alone do not establish permission
to modify the oracle or land unattended.

The memory ownership and retention policy, recovery and replay controls, stop exceptions and hard
cap, destination checks and fixture receipts above are kit requirements. The presentation does not
demonstrate that its systems implement those controls in this form.
