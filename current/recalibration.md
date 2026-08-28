---
name: recalibration
description: Reconstruct the global state of long-running work into independent working lines and their working stacks. Use when the user asks where the work stands, what has been done, what comes next, how tasks evolved, or how to regain focus after long or multi-task execution.
---

# Recalibration

## Purpose

Restore the user's global work orientation. Explain the whole active portfolio through its current working stacks, evidence-backed progress, selected top, next action, and compact popped-frame history.

This prompt is not for judging or paraphrasing the user's latest statement. Treat the invocation message only as a scope selector. Use a dialogue-review prompt separately when the task is to test whether the latest statement was understood or is correct.

## Evidence and authority

Reconstruct state from available conversation history and, when present:

1. user decisions for goals, priorities, acceptance, and abandonment;
2. native task state for readiness, dependencies, and execution status;
3. parent verification, actual files, diffs, tests, and published results for completion evidence;
4. master or mission ledgers as readable portfolio mirrors;
5. worker reports as evidence awaiting verification;
6. conversation inference only for explaining evolution.

If these conflict, report the conflict. Do not silently choose a convenient state.

## Build the portfolio

### 1. State the global goal

Start with one sentence in the user's task language. Assume the user remembers the task they created; restore coordinates instead of reteaching it.

### 2. Separate working lines

Create a new working line only when an item has an independent goal, completion condition, or responsibility boundary. A helper, method, stage, or temporary problem does not become a separate line merely because it recently received attention.

Keep queued, active, and blocked lines visible in the current view. Omit completed and expired lines there by default; preserve their frame-level evolution in the separate popped-frame view.

### 3. Rebuild each working stack

Within each live line, reconstruct only its current frame stack:

```text
root live frame → suspended live frame(s) → current top
```

For every live frame recover:

- **Push:** why a parent task was suspended and this context was entered;
- **Work:** what this frame must complete;
- **State:** queued, active, blocked, returned, verified, accepted, or expired;
- **Pop:** what evidence-backed condition closes this frame.

A non-root frame requires an actual context switch and one suspended parent task. Strict LIFO stack order uniquely determines the parent; do not add a separate return field. Ordinary sequential, parallel, verification, and rework tasks remain in the frame's task graph rather than becoming frames.

When an accepted or expired frame is popped, retain one compact record under its original working stack:

- **Main focus:** the frame's local goal;
- **Push:** why it was entered;
- **Result:** what it established or why it expired;
- **Evidence / live residuals:** only what is needed to understand or audit that result.

Do not expand ordinary tasks, failed attempts, or discarded options inside a popped frame unless the user explicitly requests that audit depth.

### 4. Calibrate progress

Do not collapse distinct states:

```text
planned ≠ dispatched ≠ returned ≠ verified ≠ accepted
```

Write `done` only for verified or accepted work. Preserve task evolution in its owning working stack, but keep popped frames compact and separate from the current control view. Omit chat-by-chat noise and raw orchestration logs.

### 5. Answer the current-state questions

For every live line answer:

- **Goal:** what final outcome does this line seek?
- **Stack:** which live frames lead to the current top?
- **Established:** which popped-frame results are still prerequisites of the current top?
- **Current:** what is selected, running in the background, blocked, or awaiting verification?
- **Next:** what is the smallest current action?

Then identify the portfolio's sole selected focus without treating it as a ban on asynchronous progress in other working stacks.

## Output shape

Render two views over the same underlying task and stack state. They are not separate ledgers or authorities.

### Print A — Current Stack View

```text
Global goal:
- ...

Working line A — <name>
- Goal:
- Stack: root live frame → ... → current top
- Established: <only popped results still required here>
- Current: <selected / background / blocked / verification>
- Next:

Working line B — <name>
- ...

Portfolio focus:
- Selected:
- Background:
- Queued / blocked / verification:
- Look at now:

Final sentence: <global goal + actual state + next move>
```

### Print B — Popped Frame View

Group compact popped records under the working stack that owned them:

```text
Working line A — <name>
- [popped] <main focus>
  - Push: <why this frame was entered>
  - Result: <what it established or why it expired>
  - Evidence / residual: <only when still useful>
```

This view preserves frame-level evolution without mixing it into the current stack. Do not promote ordinary completed tasks to popped frames. A small portfolio with no popped frames may omit Print B. Expand a record only when the user requests history/audit or a current conflict depends on its internals.

## Guardrails

- Do not begin with the latest worker, reviewer, run ID, or callback unless it defines the global state.
- Do not let the most recently active side line erase the main line.
- Do not dump task or ledger rows without translating them into the user's goals.
- Do not invent dependencies between useful but independent lines.
- Do not hide unresolved names, mappings, conflicts, or missing evidence.
- Do not mix popped-frame evolution into the Current Stack View.
- Do not flatten popped frames into a global history list; keep each record under its owning working stack and structural position.
- Do not let Print A and Print B maintain conflicting state; both are projections of the same native tasks, evidence, and stack structure.
- Do not perform work, change task state, or redesign the portfolio unless separately authorized; this prompt reconstructs and reports it.
- End with one short sentence that lets the user recover goal, present position, and next move.
