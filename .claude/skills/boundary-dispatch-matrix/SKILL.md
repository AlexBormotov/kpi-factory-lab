---
name: boundary-dispatch-matrix
description: Enforce a Boundary/Dispatch Matrix before moving execution across a process, thread, queue, service, worker, or transport boundary. Use when planning or reviewing a change that changes runtime execution context - a process/worker split, a queue or consumer, a background job, IPC, service extraction, a new transport, an auth boundary, or a new dispatch path into existing code. Catches the recurring failure where ambient context (auth, user/request scope, in-memory stop/hint/cancel signals, config) silently stops crossing into the new execution context and each consumer fails separately in prod. Do NOT use for pure file moves, function extraction, package reshuffling, or same-process refactors that keep the same call stack, request scope, and dispatch paths. Triggers - "worker split", "move to a background job", "new queue or consumer", "extract a service", "cross-process", "IPC", "new dispatch path", "run loop in a separate process".
---

# Boundary / Dispatch Matrix

Companion to cherny-workflow (rule 4, Verification Before Done). One rule, one artifact. The
repository's own architecture rules file is canonical when it already has a "Boundary/Dispatch
Matrix" section - use that table. If the repo has none, use the template here. This skill
enforces the artifact; it is not a second evolving copy of the rule.

## The hazard

Moving execution across a boundary (process / thread / queue / service / worker / transport)
silently drops ambient context. The new execution context does not reliably inherit request scope,
the authenticated principal, ContextVars, thread-locals, process-local singletons, or in-memory run
signals. Code that read identity or signals "from the air" now reads None or a stale default.
Because that context is consumed at many call sites, ONE relocation produces many SEPARATE prod
failures (whack-a-mole), and a canary on the single path you fixed proves nothing about the paths
you did not.

## The rule

Before writing the code, and again before merge, produce a Boundary/Dispatch Matrix. One row per
dispatch path. No row, no merge.

| Dispatch path | Prod config | Context crossing boundary | Propagation mechanism | Fail-loud guard | Test evidence | Untested prod waiver |

Account, in every row, for each context kind that used to be ambient:
- identity / user, auth principal / token lifetime, tenant / request scope
- cancellation and signal direction: stop / cancel / hints / pause / finalize / progress
- deadlines / timeouts / clock
- config / feature flags, resource id / lease (reacquire in the target; do not pass a local handle
  or in-memory object across the boundary)
- ordering / concurrency / backpressure, idempotency / retries / partial failure
- error surface, trace / log correlation

Non-negotiables:
- Every dispatch path gets its OWN row - the one you changed AND the ones you did not. The bug hides
  in the row you did not write.
- An empty Propagation, Fail-loud, or Test-evidence cell is a blocker, not a TODO. An untested prod
  path needs an explicit waiver with an owner and a follow-up issue, never a silent skip.
- Missing context must fail LOUD at boundary ingress: raise with the missing field, the dispatch
  path, the caller class, and the run id. Do not log token values or secrets, and never degrade to a
  silent default.
- Add a negative test: starting on the boundary without the required context fails before any
  downstream call.

## Why a matrix, not "be careful"

The discipline is the artifact. You catch the gap by being forced to write the row and finding a
cell you cannot fill, not by intending to remember. Validating the path you already fixed is
confirmation; the matrix forces you to falsify the paths you did not.

## Mechanics

- Put the filled table in the PR description (or design doc) before implementation; revisit it
  before merge.
- Prefer one explicit boundary context / envelope when several fields cross, created once at
  boundary ingress, over re-deriving each field per call site. Use stable ids, leases, or
  control-channel references for resources and signals.
- Reviewer rule: a boundary-moving PR with no matrix gets "request changes".

Tradeoff: a few minutes of up-front enumeration against a weekend of prod whack-a-mole. Skip only
when nothing crosses a new boundary (see the negative triggers in the description).

## Worked example: a worker split

The regression that motivated this skill. A run loop moved into a new worker process; identity and
in-memory signals stopped crossing on one dispatch path. The matrix that was never written would
have made the hole obvious:

| Dispatch path | Prod config | Context crossing boundary | Propagation mechanism | Fail-loud guard | Test evidence | Untested prod waiver |
| --- | --- | --- | --- | --- | --- | --- |
| tool-dispatched | the deployed configuration, started over the tool interface | user id, target device, hints, stop | context variable set at dispatch entry | present | a canary run that survives | - |
| web-dispatched | the same deployment, started from the web endpoint | user id, hints, stop, finalize | NONE | NONE | NONE | (blank = blocker) |

The empty bottom row is the entire incident: no propagation, no guard, no test. Writing the row
forces the question that a canary on the top row never asks.
