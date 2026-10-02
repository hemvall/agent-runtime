# Autonomous engineering-agent benchmark

The graduation scenario represents a coding agent that inspects a repository, performs multiple actions, is killed after step 3, resumes from its persisted safe boundary, encounters a transient external failure, suspends for a protected action, receives approval later and completes.

## Invariants

- protected side effects are never blindly repeated;
- lifecycle state and checkpoints, not chat history, decide where execution resumes;
- WAITING_APPROVAL / WAITING_EVENT consume no active worker;
- trace events make the crash, retry, wait, approval and completion inspectable;
- evaluation output owns steps, cost and latency metadata.

## Remaining production trade-offs

The repository deliberately implements runtime primitives rather than delegating orchestration to a workflow framework. PostgreSQL implementations must use transactions/row locks for timer claims and leases. External systems without idempotency support require reconciliation for uncertain outcomes. Shell execution should remain capability-restricted and isolated at the deployment boundary.
