from runtime.cli import run
from runtime.contracts import AgentDecision
from runtime.model import ModelAdapter


class FakeAdapter(ModelAdapter):
    def decide(self, goal: str) -> AgentDecision:
        return AgentDecision(kind="complete", final_answer=f"accepted: {goal}")


def test_cli_run_returns_zero(capsys) -> None:
    code = run("ship it", adapter=FakeAdapter())
    output = capsys.readouterr().out

    assert code == 0
    assert '"kind":"complete"' in output
    assert "accepted: ship it" in output
