# Explain Diff

This project uses an **Explain Diff** learning loop for every meaningful pull request.

The goal is not to accumulate static quiz answers. The goal is to slow implementation down until the author can explain the code that was just added.

## Session format

### 1. Background

Before the quiz, establish what problem the change solves and where it fits in the system.

For the bootstrap change:

- We are building an agent runtime, not an LLM wrapper.
- The runtime will eventually own state, tool execution, persistence, retries, approvals and recovery.
- The model is one component that proposes a next decision.

### 2. Intuition

Build a mental model before discussing individual lines:

```text
Goal
  ↓
Runtime
  ↓
ModelAdapter
  ↓
LLM
  ↓
validated AgentDecision
  ↓
Runtime decides what happens next
```

The key invariant is:

> The model proposes. The runtime controls.

### 3. Code walkthrough

Walk through the actual PR diff, focusing on why each boundary exists rather than narrating syntax.

For this change:

- `runtime/contracts.py` defines the typed language crossing the model/runtime boundary.
- `runtime/model.py` isolates provider-specific model integration behind `ModelAdapter`.
- `runtime/cli.py` is only an entry point; it is deliberately not an orchestration loop.
- `tests/` encode invariants such as rejecting incomplete or unexpected decisions.
- `pyproject.toml` makes the package installable and exposes the CLI.

### 4. Interactive quiz

The quiz happens **interactively**, not as a list with answers in this repository.

Rules:

1. Ask exactly five medium-difficulty free-response questions.
2. Ask one question at a time.
3. Wait for the learner's answer before continuing.
4. Evaluate the reasoning, not exact wording.
5. If the answer exposes a misunderstanding, explain that gap and ask a targeted follow-up before moving on.
6. Prefer questions about architectural consequences and failure modes over syntax trivia.
7. Do not reveal all questions or answers upfront.

### 5. Completion

The Explain Diff session is complete when the learner can explain:

- what problem the PR solves;
- how data/control flows through the changed code;
- why the chosen abstractions exist;
- at least one plausible failure mode;
- how this PR prepares the next step.

## Bootstrap change: concepts to probe

The interactive session for this PR should test understanding of:

- why `ModelAdapter` is a boundary rather than the orchestrator;
- why LLM output is validated into domain contracts;
- the difference between `ToolCall` and `ToolResult`;
- why malformed model output must fail before execution;
- why the actual observe → decide → act loop belongs in the next issue.

Do not store model answers here. The learner should reconstruct the explanation from the code and discussion each time.
