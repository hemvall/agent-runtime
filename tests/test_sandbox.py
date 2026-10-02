from pathlib import Path
import pytest
from runtime.sandbox import SandboxPolicy, SandboxViolation, redact_secrets

def test_path_traversal_is_blocked(tmp_path:Path):
    with pytest.raises(SandboxViolation): SandboxPolicy(tmp_path).path("../secret")

def test_shell_injection_and_secret_leak_are_blocked(tmp_path:Path):
    p=SandboxPolicy(tmp_path)
    with pytest.raises(SandboxViolation): p.command("rm -rf /")
    assert redact_secrets("key=abc",{"API_KEY":"abc"})=="key=[REDACTED]"
