from runtime.planning import Plan, Subtask, SubtaskStatus

def test_dependencies_and_replanning_are_runtime_owned():
    p=Plan(1,{"inspect":Subtask("inspect","inspect repo"),"fix":Subtask("fix","fix",{"inspect"})})
    assert [s.id for s in p.runnable()]==["inspect"]
    p.set_status("inspect",SubtaskStatus.COMPLETED)
    assert [s.id for s in p.runnable()]==["fix"]
    p.replan([Subtask("alternative","try alternative")])
    assert p.version==2
