# The coaching layer

Six change tools come from Kanban coaching practice. They are **not** part of the factory. They are
what the person running the engagement uses to get an organization through the build without it being
rejected. Keep them separate: the factory is made of binary gates that machines evaluate, these are
instruments for people.

## The unit is a delivery path, not a repository

A factory is a property of **one delivery path**: from the request that starts work, through the
repositories the change actually touches, the pipeline that checks it, the trunk it lands on, the
control that exposes it, to the consumer that receives the result. A path routinely crosses several
repositories and more than one team. A repository is where evidence is read, not what is being built.

This has three consequences that the rest of this file depends on.

**Time is per path, and the estate is many paths.** The first path is the expensive one, because the
method, the conventions and the discipline are being established at the same time as the mechanism.
Weeks is the right order of magnitude for that first one on a codebase already at level two or above.
Every later path is cheaper, because only the path-specific work repeats. How long the whole estate
takes is a function of how many paths it has, and that is a planning question, not a promise.

**What repeats per path, and what is built once.** Repeating: the scope decision, the risk exclusions,
the oracle and its negative control, the size ceiling taken from that path's own history, the
reconciliation of terms across its boundaries, and the gates with their named fallbacks. Built once
and shared: the method itself, the instruction and context file conventions, the evaluation discipline
for the harness, and this coaching layer.

**A path maps to what the source tools call a service.** That correspondence is what makes the six
usable at all: their unit of engagement is a service or a set of services, explicitly not a team, and
their scaling rule is one service at a time. Read service as delivery path throughout and the tools
transfer without distortion.

The distinction matters because importing them into the method would damage it. Two places where
that is certain:

- **The litmus test is not an oracle.** Its questions are judged by a human. Gate G4 requires a check
  that is cheap, frequent and unfakeable at once. Replacing a machine verdict with a human reading
  destroys the rule that autonomy is granted only as far as it can be verified cheaply.
- **"Start with what you do now" would remove G5 and G7.** If existing process is left untouched to
  avoid stress, the approval chain and the protected check cannot be required. Waiting for them to
  appear on their own removes the basis for unattended work.

## The six, and what we do with each

| Tool | Verdict | Where it attaches |
| --- | --- | --- |
| STATIK | adapt, this is the entry procedure | before G1, feeding G1, G2 and the audit |
| Evolutionary Change Model and its litmus test | adapt, this is the survival check | after handover, and whenever a gate looks decorative |
| Scaling Principles | adopt as a stated rule | after the first proven task class |
| Cadences | adopt, and name the decision each one produces | the whole engagement, every path |
| Change Management Principles | adopt one clause only | before the intent chain is set up |
| Service Delivery Principles | keep as the systems lens | wherever a path crosses authorities: G4, G7, G8, G9 |

### STATIK, adapted

The published form guides "towards a service-oriented system" and ends with "Socialize design &
negotiate implementation". Our version, run in week one:

Pick one class of change and its terminal consumer. Name the product outcome it must produce. Pull
the sources of dissatisfaction and of demand out of issues, incidents, CI history and merge history,
not out of a conversation. Measure current capability on the applicable pillars. Draw the path from
intent through code, CI, trunk and the production signal. Classify the work against G1 scope, G3 risk
and the repository's own size ceiling. Design the loop, the harness, the oracle and gates G4 to G9.
Then agree the first pilot class and the named human fallback for every gate that does not pass.

The last step is the one teams skip and the one that decides adoption. A design nobody agreed to is
bypassed in week five.

### The litmus test, adapted

The original asks four questions to detect a false summit: whether manager behaviour, the customer
interface, the customer contract or the delivery business model actually changed. Ours must be
answerable from the repository and the pipeline, never by asking the team.

1. **How many trunk updates in the last 30 days landed with no human reading the diff?** Zero means
   the nine gates are decoration.
2. **Is there a stored negative-control run** where disabling the behaviour turned exactly the
   covering tests red, they went green on restore, and the artifact checked is the one the consumer
   receives? Without it the green build is not an oracle.
3. **Has the protected check ever gone red and stopped a landing?** Never means it is untested or
   bypassable. Check also that the landing principal cannot alter or remove it.
4. **Does the history show one full trace, base commit to candidate to landed commit to production
   outcome,** with a failure fixture showing the line stopping, the revert to the last green commit,
   the checks rerunning, and a new intent written? Without it the harness produces commits but the
   factory does not close.

Ask question one a month after handover. A factory nothing has passed through by itself is not
built, whatever the audit said.

### Scaling Principles, adopted

"Scale out in a service-oriented fashion one service at a time." Our unit of expansion is one bounded
task class on one delivery path. Two axes expand independently and should not be confused: more
classes of change on a path already proven, and more paths. Widen one at a time. Every next class re-runs the gates,
its own size ceiling, its own negative control. A cross-repository path also runs the vocabulary
gate. Do not copy the previous pilot's configuration without a fresh audit: the measured ceilings
differed across three repositories of one team.

Expansion starts only after the previous class produced an observed landed commit and a G9 outcome.

### Cadences

The purpose is stated as enabling an organization "to evolve in a very organic fashion". A cadence is
inspect and adapt on a fixed rhythm: it has an input, an output, and a decision taken at it. Anything
that only reports is not a cadence, whatever it is called.

Our engagement already runs on a rhythm. What the tool adds is the requirement to name, for each
cadence, the decision it exists to produce, and to write that decision down where the next cadence can
see it. Candidates, from fastest to slowest: which candidate goes back to the loop; which gate is
blocking and what its fallback cost; which task class expands next; which ceiling moves; which
evaluation is added after an incident; whether the path is finished and which path is next.

The failure to watch for is the opposite of the one in the tool: a rhythm that meets, decides nothing
and is still called a cadence. The receipt is that each meeting leaves a recorded decision, not that
it happened.

### Change Management Principles, one clause

Take "Respecting existing roles, responsibilities & job titles" and nothing else. Gate owners must be
the people who already hold that authority. A fallback assigned to a role invented for the diagram is
a fallback that will be bypassed. The rest of this tool assumes an organizational transformation over
quarters, which is not what a four-week build is, and promising it makes the timeline unserious.

## Two failure modes, in factory terms

**Overreaching.** More autonomy granted than the gates support. The pattern: a call path crosses two
repositories, only one was audited, local CI is green, but scope does not cover the whole path, the
oracle does not check the boundary contract, and the evidence carries no commit for the second
repository. Or the candidate exceeds the repository ceiling and lands anyway. Response: stop at the
first failing gate and take its named fallback.

**False summit.** Every standard file exists, CI is green, agent changes are being produced, so the
rollout is declared a factory. But the negative control does not turn the right tests red, or the
pipeline checks a different artifact than the consumer receives, or the protected verdict is not tied
to the exact landed commit, or a production breach neither stops the line nor returns as a new
intent. A loop and part of a harness are present; the stream-level factory is not. Comprehension debt
grows the whole time with the suite green.

## What not to take

- **Not the maturity scale.** The model these tools come from has seven levels, zero to six, and its
  own catalogue of transition practices. We keep our five levels and eleven pillars. Take the
  mechanism, stress then reflection then leadership then consolidation, not the ladder.
- **Not disruption of production, and not human discomfort, as a stressor.** Ours are an isolated
  negative control, a fixture, or a bounded candidate. G3 excludes the dangerous classes, G5 requires
  isolation, G8 separates landing from exposure, G9 requires recovery.
- **Not the classification of resistance as bad faith, and not the discussion of who leaves.**
  Repository evidence establishes no motives, and this engagement carries no authority over staffing.
- **Not the litmus test or cadences as a measure of comprehension debt.** Both detect the absence of
  operational change. Neither measures how much of the code anybody understands. That gap stays open
  and stays declared.

## Sources and attribution

The six tools are from Kanban coaching practice as taught in the Kanban Coaching Professional
material, Kanban University, 2023 edition, read on 2026-08-25, and from "Kanban Maturity Model:
Evolving Fit-For-Purpose Organizations" by David J. Anderson and Teodora Bozheva. The elements taken
are: the systems-thinking approach to introducing a service, through purpose, dissatisfaction,
demand, capability, workflow, classes of service, system design and the negotiation of adoption; the
service delivery principles and their premise that an organization is a network of interdependent
services governed by policies; the scaling rule to expand one service at a time; cadences as a
management system that turns improvement into a repeating cycle rather than a one-off redesign; the
change management principles, of which one clause is adopted here; the evolutionary change model with
its sequence of stressor, reflection, leadership and consolidation; the litmus test as a smoke test
for a false summit; and the naming of the two failure modes, overreaching and the false summit
plateau.

Two facts about the source model are stated here because they bear on how the tools are used, and
both were verified against the book and the slides rather than taken second hand. It defines seven
maturity levels numbered zero through six, not five. A level splits into a transition stage and a core
stage, served by two distinct classes of practice, which is why skipping is warned against: the
purpose is to avoid overreaching, and the preparatory class exists to make the next level adoptable.

Not from those sources, and belonging to this kit: the four litmus questions, each rewritten to be
answerable from a repository and a pipeline rather than from a conversation with the team; the
adapted entry sequence and its ordering against the gates; the observation that our own cadences are
reporting rather than feedback, and the requirement that each one end in a named decision; the two
failure modes restated in terms of gates, commits and evidence; and the exclusion list, in particular
the refusal to import the seven-level scale, to use production disruption or human discomfort as a
stressor, and the statement that neither the litmus test nor cadences measure comprehension debt.

The maturity scale of the source model is deliberately not imported. This kit keeps its own five
levels and eleven pillars. What transfers is the mechanism, not the ladder.
