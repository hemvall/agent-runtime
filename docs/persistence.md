# Persistence model

PostgreSQL is the authoritative source for run lifecycle, completed steps, tool-call lifecycle, transitions and artifact references.

Model context is **derived**. It is rebuilt from persisted structured state and observations; losing a prompt buffer must not lose execution state. Summaries and rendered context are caches/artifacts and may be regenerated.

External systems remain authoritative for their own side effects. A database row saying a tool was requested is not proof that an external side effect did or did not happen; issue #6 adds explicit crash-boundary semantics for that gap.
