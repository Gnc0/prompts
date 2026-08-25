---
name: recalibration
description: Reconstruct the global state of long-running work into independent working lines and their working stacks. Use when the user asks where the work stands, what has been done, what comes next, how tasks evolved, or how to regain focus after long or multi-task execution.
---

# Recalibration

## Purpose

Restore the user's global work orientation. Explain the whole active portfolio: its original goals, independent working lines, nested stack frames, evidence-backed progress, current top, next action, and return point.

This skill is not for judging or paraphrasing the user's latest statement. Treat the invocation message only as a scope selector. Use a dialogue-review skill separately when the task is to test whether the latest statement was understood or is correct.

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

Keep inactive, blocked, completed, and expired lines visible when they still explain the current portfolio.

### 3. Rebuild each working stack

Within each line, order frames from the root goal to the current top:

```text
root goal → entered stage → discovered problem → evolved subproblem → current top
```

For every relevant frame recover:

- **Push:** why the parent work paused;
- **Work:** what this frame must complete;
- **State:** queued, active, blocked, returned, verified, accepted, or expired;
- **Pop:** what completes the frame;
- **Return:** where work resumes afterward.

Do not call something a stack frame when it has no return point.

### 4. Calibrate progress

Do not collapse distinct states:

```text
planned ≠ dispatched ≠ returned ≠ verified ≠ accepted
```

Write `done` only for verified or accepted work. Preserve the causal changes that explain the current structure, but omit chat-by-chat noise and raw orchestration logs.

### 5. Answer the three questions

For every active line answer:

- **Goal:** what final outcome does this line seek?
- **Done:** which frames are evidence-backed and already popped?
- **Next:** what is the smallest current action, and where does work return after it?

Then identify the portfolio's current sole focus and keep other lines visible without giving them equal narrative weight.

## Output shape

Adapt length to the portfolio. Prefer this structure:

```text
Global goal:
- ...

Working line A — <name>
- Goal:
- Evolution:
- Stack: root → frame → current top
- Done:
- Current:
- Next:
- Pop / return:

Working line B — <name>
- ...

Portfolio focus:
- Current sole focus:
- Queued / blocked / expired:
- Look at now:

Final sentence: <global goal + actual state + next move>
```

A small portfolio may use a compact table. Expand history only when it explains a current line, dependency, or return point.

## Guardrails

- Do not begin with the latest worker, reviewer, run ID, or callback unless it defines the global state.
- Do not let the most recently active side line erase the main line.
- Do not dump task or ledger rows without translating them into the user's goals.
- Do not invent dependencies between useful but independent lines.
- Do not hide unresolved names, mappings, conflicts, or missing evidence.
- Do not perform work, change task state, or redesign the portfolio unless separately authorized; this skill reconstructs and reports it.
- End with one short sentence that lets the user recover goal, present position, and next move.
