# Agent Runtime

A reusable execution layer for building **long-running, production-grade AI agents**, built from first principles so every important runtime concept can be understood, tested and explained.

The goal of this repository is twofold:

1. **Build a real agent runtime** that can power different domain agents.
2. **Learn how production agent systems actually work** by implementing the orchestration layer ourselves instead of hiding it behind an agent framework.

## What are we building?

The runtime is the infrastructure underneath agents such as:

```text
┌───────────────────────────────────────────────────────┐
│                    DOMAIN AGENTS                      │
│                                                       │
│   Coding Agent       Sales Agent       Support Agent  │
│        │                  │                  │         │
└────────┼──────────────────┼──────────────────┼─────────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            ▼
┌───────────────────────────────────────────────────────┐
│                     AGENT RUNTIME                     │
│                                                       │
│  Agent loop          State machine                    │
│  Persistence         Checkpoints / resume             │
│  Human approval      Events / webhooks / timers       │
│  Retry / idempotency Context management               │
│  Budgets             Observability / replay           │
│  Permissions         Sandboxed execution              │
└───────────────────────────┬───────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────┐
│                         TOOLS                         │
│                                                       │
│ GitHub │ Shell │ Files │ Email │ CRM │ APIs │ DB │ … │
└───────────────────────────────────────────────────────┘
```

A Coding Agent and a Sales Agent have completely different jobs and tools, but both need the same hard infrastructure: persistent execution state, crash recovery, retries, human approval, asynchronous events, budgets, permissions and traces.

That reusable infrastructure is what this repository builds.

## Why does this need a runtime?

A basic agent can be written as:

```text
prompt → LLM → tool → LLM → tool → result
```

That works for demos. Production work creates harder problems.

What happens when:

- the task lasts several hours or days?
- the worker crashes after an external action succeeds?
- an API returns 500 halfway through the task?
- the agent must wait six hours for a human?
- a webhook should wake the task tomorrow?
- two workers try to resume the same run?
- an action must never execute twice?
- model context becomes too large?
- the agent wants to perform a dangerous action?
- we need to reconstruct exactly why a run failed?

Those are runtime problems, not prompt problems.

## Example: Coding Agent

A Coding Agent could receive:

> Add rate limiting to this API, write the tests, run them and prepare a pull request.

It may inspect dozens of files, edit code, execute tests, observe a failure, correct the implementation and try again.

If its worker dies after action 20, the runtime should restore the persisted run and safely continue instead of restarting the task.

If the agent eventually wants to merge or deploy, a policy can move the run into `WAITING_APPROVAL`. No process needs to remain alive while a human decides. Approval can arrive hours later and wake the same run.

## Example: Sales Agent

The same runtime could power a completely different workflow:

```text
qualify company
      ↓
inspect CRM
      ↓
prepare outreach
      ↓
WAITING_APPROVAL
      ↓
send email
      ↓
WAITING_EVENT
      ↓
reply received
      ↓
resume run
      ↓
prepare next action
```

The Sales Agent supplies its own tools, instructions and policies. The runtime still handles persistence, waiting, resuming, retries and observability.

## Separation of responsibilities

Domain agents define:

- the job to accomplish;
- available tools;
- domain instructions;
- domain-specific policies and context.

Agent Runtime defines:

- how a run progresses;
- how state is persisted;
- how actions are executed safely;
- how interrupted work resumes;
- how external events wake runs;
- how approvals suspend execution;
- how failures and retries behave;
- how budgets and permissions are enforced;
- how execution is traced and evaluated.

The goal is to eventually be able to write something conceptually similar to:

```python
coding_agent = Agent(
    runtime=runtime,
    tools=[github, filesystem, shell],
    policies=[approve_before_merge],
)

sales_agent = Agent(
    runtime=runtime,
    tools=[crm, email],
    policies=[approve_before_send],
)
```

The agents change. **The execution infrastructure does not.**

## Core principle

> **The model proposes. The runtime controls.**

An LLM is not trusted as the orchestrator. Its output crosses a typed validation boundary before the runtime decides what happens next.

Over the course of the project, that principle expands into state machines, persistence, checkpoints, idempotency, human-in-the-loop interrupts, event-driven execution, context management, observability and security.

## Learning by building

This repository deliberately avoids jumping straight to a high-level agent framework.

The point is to implement the important primitives ourselves first so concepts such as durable execution, idempotency, state recovery and human interrupts are understood rather than treated as framework magic.

Each major pull request therefore has two outputs:

- a working piece of the runtime;
- an **Explain Diff** session used to understand the background, intuition, code changes, architectural trade-offs and failure modes introduced by that PR.

The learning process is part of the project, but the codebase is intended to converge toward a coherent, reusable runtime rather than a collection of isolated exercises.

## Roadmap

The repository grows toward the complete runtime in stages:

1. typed runtime contracts and model boundary;
2. observe → decide → act loop;
3. explicit state machine;
4. persistent runs and execution history;
5. checkpoints, crash recovery and idempotency;
6. human-in-the-loop interrupts;
7. asynchronous events, webhooks and durable timers;
8. bounded context and compaction;
9. planning, retries, timeouts and budgets;
10. tracing, deterministic replay and evaluations;
11. concurrency, permissions and sandboxing;
12. end-to-end production benchmark.

## Final benchmark

The runtime should eventually execute a realistic software-engineering task end to end while we deliberately:

1. kill its worker mid-run;
2. restart it;
3. inject an external failure;
4. force it to wait for human approval;
5. leave it suspended;
6. approve the action later;
7. let it resume and complete.

If that works without losing state or blindly repeating protected side effects, we have moved well beyond a toy agent loop.

The final proof of the abstraction is to run **multiple different agents on the same runtime** without pushing their domain-specific logic into the runtime itself.
