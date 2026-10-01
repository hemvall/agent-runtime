# Agent Runtime

A learning project for building **production-grade agentic systems** from first principles.

The goal is not another RAG pipeline or a thin LLM wrapper. The runtime should eventually execute long-running tasks, persist and recover state, wait for external events, request human approval for risky actions, enforce budgets and policies, and expose enough traces to understand and replay failures.

## Final benchmark

Given a software-engineering task, the agent can inspect a repository, plan work, edit files, execute tests, recover from failures, pause before sensitive actions, resume after approval, and prepare a pull request.

The runtime must survive process crashes without corrupting state or blindly repeating non-idempotent actions.

## Learning constraints

- Python, FastAPI, Pydantic and PostgreSQL are the initial stack.
- No LangGraph, CrewAI or equivalent orchestration framework during the foundations.
- State, memory and model context are separate concepts.
- Every phase ends with an observable acceptance test.
- Reliability is part of the runtime, not something added after the agent works.

## Target architecture

```text
User/API
   |
Task Manager
   |
Agent Runtime ---- Policy Engine ---- Human approval
   |     |
   |     +---- Context / checkpoints
   |
Tool Executor ---- sandbox / APIs
   |
Event system ---- queue / webhook / timer
   |
Persistent state
```

## Roadmap

1. Agent loop from scratch
2. Explicit state machine
3. Persistent runs and steps
4. Durable execution and recovery
5. Human-in-the-loop
6. Events, timers and asynchronous work
7. Long-context management
8. Planning and replanning
9. Reliability and budgets
10. Observability and replay
11. Agent evaluations and fault injection
12. Production hardening

Issues contain the implementation exercises and acceptance criteria.
