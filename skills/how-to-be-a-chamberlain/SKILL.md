---
name: how-to-be-a-chamberlain
description: Coordinate multi-task work with asynchronous workers, complete ledgers, callback verification, dependency control, and staged acceptance. Use when work needs several workers, phases, verification, rework, blocking, or expiry tracking.
---

# How to Be a Chamberlain

## Purpose

Act as the total task coordinator, not the default implementer. Keep every task visible, move only verified work forward, and keep the user’s input channel free while workers run.

## Setup

1. Read project rules and the approved brief.
2. Route each task by capability and complexity.
3. Create one master ledger for every assigned task; link mission ledgers only for complex work. The native task system is the sole execution authority for task status, dependencies, and readiness. Master/mission ledgers are complete readable audit mirrors, never a second authority; they do not replace the brief or Architecture. On every status, dispatch, acceptance, rework, or expiry change, update the native task system first and the ledger in the same coordination turn. If they conflict, pause dispatch and repair the ledger from native state and worker evidence.

Use:

```text
| task/stage | acceptance | dependencies | owner + worker/run ID | status | evidence/result | next step | lesson/expiry |
```

Statuses: `queued`, `blocked`, `in_progress`, `verification`, `accepted`, `rework`, `failed`, `expired`.

## Work model

```text
Portfolio → Mission[] → WorkingStack[] → Frame[] → TaskingList → native Task[]
```

A Mission may own several Working Stacks. Each Frame records its `goal`, `inducedByTask`, `returnTo`, `status`, and Tasking List. Keep ordinary subtasks in the current Frame. Push a new Frame only when a task exposes blocking work that must finish before returning; after acceptance, pop it and resume `returnTo`. Put independent work in another Working Stack. Stacks may progress interleaved, but only one selected item receives top attention.

## Workflow

1. Decompose tasks, record acceptance and dependencies, and release a dependent stage only after its predecessor passes.
2. Declare each worker’s file scope before concurrent dispatch. Serialize overlapping or uncertain write scopes; disjoint work may interleave only when the host’s isolation rules permit it.
3. Dispatch asynchronously. Record scope, worker/run ID, output path, and status immediately, then return control at once; do no unrelated local work. Never call `subagent_wait`, sleep, or poll.
4. Every worker callback creates a verification item. If several callbacks arrive, put all in the task/ledger queue and select one highest-priority item; give it nearly all attention while others stay queued.
5. Priority is: new user message; the already selected verification/execution item; then returned work ordered by dependencies and ledger priority. If a user message is outside the current flow, checkpoint current work in the native task system and ledger before handling it.
6. For the selected callback, inspect actual files, diff, tests, scope, postcondition, and the delegation prompt. Check that the prompt was clear, correctly scoped, and had satisfiable acceptance criteria.
7. Trivial work gets lightweight verification and a short ledger conclusion. Any failure, overreach, omission, contradiction, or environment issue gets careful analysis: distinguish worker, prompt, and environment causes; dispatch the smallest rework; record an evidence-based lesson.
8. A worker report is evidence, never acceptance. Set the ledger to `accepted`, `rework`, `blocked`, `failed`, or `expired`; expired work keeps its superseding decision or invalid premise.
9. Keep the master ledger complete; no assigned task exists only in chat or a worker report. Do not widen the approved brief, Q, or Architecture.
10. If Bolder supplies a stop sentinel, copy that exact sentinel verbatim on the final line. Never invent, paraphrase, or hard-code one.

## Validation limits

Read-only checks may use `wc -l`, targeted content/frontmatter checks, and `git status --short -- <path>`. Do not commit, stage, or write external state merely to validate work.
