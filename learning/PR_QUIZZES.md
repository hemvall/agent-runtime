# PR Learning Quiz

The project is intentionally built as a learning exercise. Every meaningful PR should include a **Learning Review** comment explaining what changed, why the design was chosen, and what concepts should be understood before merging.

## Workflow

1. Read the issue before looking at the implementation.
2. Review the PR diff.
3. Read the Learning Review comment.
4. Answer the PR quiz **without looking at the answers or asking an AI first**.
5. If an answer is unclear, revisit the relevant code.
6. Merge only when you can explain the important design choices in your own words.

## Bootstrap runtime contracts and CLI

### Questions

1. Why does the runtime define a `ModelAdapter` instead of importing one LLM SDK directly everywhere?
2. What problem does `AgentDecision` solve compared with asking the model to return arbitrary prose?
3. Why are `ToolCall` and `ToolResult` two different models?
4. What does `extra="forbid"` protect us from?
5. Why does a `tool` decision require `tool_call`, while a `complete` decision requires `final_answer`?
6. Why is `DemoModelAdapter` deterministic?
7. Which part of this PR is the actual orchestration loop?
8. If we replace one LLM provider with another later, which abstraction should isolate most of that change?
9. What should happen if model output does not satisfy the contract?
10. Why is issue #2 deliberately separate from this bootstrap work?

### Practical challenge

Without modifying the contracts, implement a second fake adapter in a test that returns:

```text
kind = complete
final_answer = "42"
```

Then explain why the CLI does not need to know which adapter produced the decision.

## Rule for future PRs

Each major PR should add its own quiz section here or in a dedicated file under `learning/`, and the PR conversation should contain a Learning Review with:

- mental model;
- important files;
- design choices;
- failure modes;
- what to remember;
- quiz questions.
