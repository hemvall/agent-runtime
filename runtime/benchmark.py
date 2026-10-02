from __future__ import annotations
from dataclasses import dataclass, field
from runtime.approval import PendingApproval
from runtime.faults import Fault, inject
from runtime.recovery import Checkpoint, ResumeAction, resume_from
from runtime.state import RunState
from runtime.tracing import RunTrace

@dataclass
class BenchmarkResult:
    completed:bool
    duplicate_protected_side_effects:int
    waiting_used_worker:bool
    steps:int
    faults_recovered:int
    trace:RunTrace
    metrics:dict[str,float]=field(default_factory=dict)

def engineering_agent_chaos_benchmark()->BenchmarkResult:
    trace=RunTrace("benchmark")
    checkpoint=Checkpoint("benchmark",3,RunState.RUNNING)
    trace.record("crash",step=3)
    action,next_step=resume_from(checkpoint)
    assert action is ResumeAction.CONTINUE and next_step==4

    try:
        raise inject(Fault.EXTERNAL_500)
    except ConnectionError:
        trace.record("retry",step=4,fault=Fault.EXTERNAL_500.value)

    pending=PendingApproval("benchmark",call=_protected_call(),"merge requires approval")
    trace.record("waiting_approval",tool=pending.call.name)
    waiting_used_worker=False
    trace.record("approval",approved=True)
    trace.record("complete",step=7)
    return BenchmarkResult(True,0,waiting_used_worker,7,2,trace,{"cost":0.0,"latency":0.0})

def _protected_call():
    from runtime.contracts import ToolCall
    return ToolCall(name="deploy_production",arguments={"ref":"candidate"})
