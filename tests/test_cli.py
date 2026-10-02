from runtime.cli import run
from runtime.contracts import AgentDecision, Observation
from runtime.model import ModelAdapter


class FakeAdapter(ModelAdapter):
    def decide(self, goal: str, observations: list[Observation]) -> AgentDecision:
        return AgentDecision(kind="complete", final_answer=f"accepted: {goal}")


def test_cli_run_returns_zero(capsys) -> None:
    code = run("ship it", adapter=FakeAdapter())
    output = capsys.readouterr().out

    assert code == 0
    assert '"final_answer": "accepted: ship it"' in output
    assert '"steps": 0' in output
