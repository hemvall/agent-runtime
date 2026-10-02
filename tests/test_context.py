from runtime.context import ContextBuilder, ContextItem

def test_context_is_bounded_and_deterministic():
    durable=[ContextItem("goal","fix tests",10,100)]
    history=[ContextItem(f"s{i}",f"step {i}",10,i) for i in range(120)]
    a=ContextBuilder(50).build(durable,history)
    b=ContextBuilder(50).build(durable,history)
    assert a==b
    assert a.token_count<=50
    assert len(a.items)<len(history)
    assert any(i.key=="goal" for i in a.items)
