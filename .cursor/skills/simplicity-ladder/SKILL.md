---
name: simplicity-ladder
description: Stop at the first rung that solves the problem before writing code, and keep the ladder inside the boundary of the standing architectural decision. Use when about to add code, choose a library, introduce an abstraction, add a configuration knob, or when a cheaper path appears through a different tool than the one already chosen. Catches two failures - overbuilding past the request, and silent architectural drift where "already installed and working" quietly outweighs the decision on record. Do NOT use it to justify simplifying security, input validation, error handling, data-loss protection, or accessibility, and do NOT use it as permission to swap a chosen tool. Triggers - "should I build this", "which library", "add an abstraction", "there is a simpler way", "we already have X installed", "just use Y instead", "minimum code", "YAGNI", "reuse before you build", "do we need this dependency".
---

# Simplicity ladder

Two rules that only work together. The ladder says stop early. The boundary says
stop early **within the decision already made**. The ladder without the boundary
turns "already installed and working" into the highest-weighted architectural
criterion, silently.

## 1. Order of precedence

Resolve in this order. A lower item never overrides a higher one.

1. Hard requirements and the standing architectural decision.
2. The simplest implementation compatible with them.
3. If the simplest implementation needs a different tool, that triggers an
   explicit revision of the decision, not a quiet switch.

## 2. The ladder

Before writing code, stop at the first rung that holds.

The ladder runs after the problem is understood, not instead of it. Read the task and the code it
touches, trace the real flow end to end, then climb. The smallest diff in the wrong place is not a
lower rung, it is a second defect.

| Rung | Test |
|---|---|
| 1. Do not build | The request does not actually require it. YAGNI. |
| 2. Reuse | Something that already exists covers it, checked in this order: a helper, utility or pattern already in this codebase; the standard library; a native platform feature; an already-installed official dependency. |
| 3. Build minimal | Custom code is genuinely needed. Write the smallest clear version. |

Rung 2 is scoped by section 1. "Already installed" qualifies only if it sits
inside the standing decision. Otherwise it is a candidate for revision, not a
free rung.

## 3. The gate

- **WHEN** about to write the first line of new code, add a dependency,
  introduce an abstraction, or add a configuration knob.
- **DO** name the rung being taken and state, in one line, why the rung above it
  does not hold.
- **RECEIPT** that one line exists before the code does, and it names the
  standing decision the rung sits inside.
- **ELSE** status is `rung unjustified`. Do not write the code yet.

The receipt is one sentence, not a document. "Rung 3: no stdlib primitive for
weighted retry with jitter; stays inside the chosen httpx client."

## 4. Counterfactual test for drift

Before the first action that favours an alternative tool, ask:

> Would this action be needed if the standing decision definitely holds?

If **no**, this is adoption, not repair. Stop. Either return to the decision, or
open an explicit revision.

A legitimate revision has all four parts: a new fact, the original criterion that
fact affects, the full new trade-off, and the owner's confirmation. If the
sentence "this new fact changes original criterion X" cannot be completed, it is
drift. "Easier" and "already works" are not criteria unless speed of adoption was
a criterion in the original choice.

**Default when the test trips:** stop and ask, in one line, before doing the
work. State the cheaper path, the criterion it would overturn, and wait. Do not
build both, and do not build the cheaper one to "show" it.

## 5. Marking intentional simplification

Any deliberate simplification carries a short comment with a named ceiling and an
upgrade path.

```
# O(n^2) is fine while n < 100 (single tenant); upgrade: index by tenant_id
```

No ceiling means it is not a deliberate simplification, it is an unexamined one.

## 6. Never simplify

Security. Input validation. Error handling. Data-loss protection.
Accessibility.

These are not on the ladder. A cheaper option here is not a lower rung, it is a
defect. Related: a silent fallback on a failed precondition hides the root cause;
set explicit error state instead.

## 7. Worked failure

A local runtime was chosen. A different runtime was repaired on request as a
scoped subtask. Rung 2 then argued "prefer the already-installed thing", and work
began building integration against the repaired runtime, against the decision on
record.

Nothing in that sequence felt like a decision. Each step was locally reasonable,
and no moment of "I am switching" ever occurred. That is why the counterfactual
test in section 4 is an external check rather than a matter of attention.

## 8. Repo maturity tightens the rungs

The link runs one way: the lower the repository maturity, the stricter the ladder
must be applied. Low maturity means weak checkers, so an unjustified rung 3 is
less likely to be caught before it ships. In a high-maturity repository, more
custom code is survivable because the oracles are real.

## 9. What this skill is not

- Not a reason to under-deliver on the requested scope. The ladder governs how
  something is built, never whether the ask is honoured in full.
- Not a review of existing code. It fires before writing, not after.
- Not applicable to pure refactors that keep the same tool, same contract, and
  same execution context.

## 10. Sources and attribution

The ordered pre-code ladder, and the rule that the safety-critical categories are carved out of it,
come from **Ponytail** by Dietrich Gebert (`github.com/DietrichGebert/ponytail`, `ponytail.dev`),
a behaviour rule set for coding agents. Observed 2026-08-21 through the GitHub API: created
2026-06-12, MIT licence, release v4.9.0 published 2026-08-07. Its own framing is a ladder climbed
before any code is produced, and it separates security, trust-boundary validation, accessibility and
data-loss handling from anything the ladder is allowed to reduce. This file compresses its checklist
into three rungs and keeps that separation as section 6. Two items were added on 2026-09-07 from
the v4.9.0 rule text: reuse inside the codebase as the first thing to check on rung 2, and the rule
that the ladder is climbed only after the problem is understood.

The underlying principles are older than that project and are not attributable to it: YAGNI, reuse
before build, and prefer the standard library are long-standing practice. What is taken is the
ordered form and the explicit carve-out.

Not from that source, and belonging to this kit: the order of precedence in section 1 that puts the
standing architectural decision above the ladder, the counterfactual drift test in section 4, the
one-line receipt in section 3, the named-ceiling rule in section 5, the maturity coupling in
section 8, and the worked failure in section 7.
