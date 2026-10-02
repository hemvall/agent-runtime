from runtime.faults import Fault, RECOVERY_MATRIX, inject

def test_every_fault_has_protected_side_effect_invariant():
    assert set(RECOVERY_MATRIX)==set(Fault)
    assert all(i.protected_side_effects_not_duplicated for i in RECOVERY_MATRIX.values())

def test_timeout_injection_is_retry_classifiable():
    assert isinstance(inject(Fault.TOOL_TIMEOUT),TimeoutError)
