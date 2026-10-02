# Tool crash-boundary semantics

A protected side effect uses a stable idempotency key derived before execution. A recorded success is never executed again. If the worker dies after the external system accepts the action but before success is committed, the outcome is **UNCERTAIN**, not “failed”.

For idempotency-aware providers, retry with the same key gives effectively at-most-once side effects. Without provider support, the runtime must reconcile/read the external state or require human resolution; blindly retrying gives at-least-once behavior and may duplicate the action.
