import json
from runtime.evals import GoldenTask, evaluate, to_json

def test_eval_is_machine_readable():
    r=evaluate(GoldenTask("t","goal","done"),lambda _:("done",{"steps":2,"tool_calls":1}))
    payload=json.loads(to_json([r]))
    assert payload[0]["success"] is True and payload[0]["steps"]==2
