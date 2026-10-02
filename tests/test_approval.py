from runtime.approval import PolicyDecision, RiskyToolPolicy, PendingApproval, resolve_approval
from runtime.contracts import ToolCall

def test_risky_action_waits_for_human():
    call=ToolCall(name="deploy_production")
    assert RiskyToolPolicy({"deploy_production"}).evaluate(call) is PolicyDecision.REQUIRE_APPROVAL

def test_rejection_becomes_agent_feedback():
    pending=PendingApproval("r1",ToolCall(name="send_email"),"external side effect")
    call, observation=resolve_approval(pending,False)
    assert call is None
    assert "rejected" in observation
