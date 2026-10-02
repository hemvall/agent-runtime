import pytest
from runtime.budgets import Budget, BudgetExceeded, BudgetLimits

def test_repeated_action_loop_is_stopped():
    b=Budget(BudgetLimits(max_identical_actions=2))
    b.charge(action="read:a"); b.charge(action="read:a")
    with pytest.raises(BudgetExceeded,match="repeated action"): b.charge(action="read:a")

def test_agent_cannot_expand_runtime_budget_by_usage():
    b=Budget(BudgetLimits(max_tool_calls=1))
    b.charge(tool_calls=1)
    with pytest.raises(BudgetExceeded): b.charge(tool_calls=1)
