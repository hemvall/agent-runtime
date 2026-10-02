# Durable timers

Workers never sleep for delayed work. A wake-up time is persisted, and a scheduler only claims due timer IDs. Claiming must be transactional in the PostgreSQL implementation so repeated scheduler ticks cannot enqueue the same wake-up twice.

Polling is simple and portable; delayed queues reduce polling but inherit broker semantics; workflow engines provide durable timers as a primitive but move orchestration ownership outside this runtime.
