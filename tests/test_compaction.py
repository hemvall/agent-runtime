from runtime.compaction import authoritative_fact, compact

def test_compaction_is_versioned_without_replacing_state():
    original=["customer=42","approval=pending","tool output "*100]
    c=compact(original,max_chars=80)
    assert c.version==1 and c.source_digest
    state={"approval":"pending"}
    assert authoritative_fact(state,"approval")=="pending"
    assert original[0]=="customer=42"
