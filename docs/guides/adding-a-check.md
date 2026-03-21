# Adding a New Guardrail Check

This guide shows how to add a new check to either the Input Guardrails or Output Validation module.

## Step 1: Create the Check File

Create a new file in `src/agentguard/input_guardrails/checks/` (or `output_validation/checks/`).

Every check must implement an async `check` function that returns a `CheckResult`:

```python
"""Detect [what your check detects]."""

from __future__ import annotations

from agentguard.common.models import CheckResult, RiskLevel


async def check(text: str) -> CheckResult:
    # Your detection logic here
    detected = False  # replace with actual detection

    if detected:
        return CheckResult(
            check_name="your_check_name",
            passed=False,
            decision="block",  # or "redact", "repair", "reject", "escalate"
            reason="Description of what was detected",
            severity=RiskLevel.HIGH,
            metadata={"details": "..."},
        )

    return CheckResult(
        check_name="your_check_name",
        passed=True,
        decision="allow",  # or "pass" for output checks
        reason="No issues detected",
    )
```

## Step 2: Register in the Engine

Add your check to the engine's `evaluate_input` (or `validate_output`) function in `engine.py`:

```python
from agentguard.input_guardrails.checks import your_check_name

# Add to the asyncio.gather call:
results = await asyncio.gather(
    # ... existing checks ...
    your_check_name.check(text),
)
```

## Step 3: Write Tests

Create tests in `tests/test_input_guardrails/` (or `test_output_validation/`):

```python
import pytest
from agentguard.input_guardrails.checks import your_check_name

@pytest.mark.asyncio
async def test_your_check_detected():
    result = await your_check_name.check("input that should trigger")
    assert not result.passed

@pytest.mark.asyncio
async def test_your_check_clean():
    result = await your_check_name.check("clean input")
    assert result.passed
```

## Step 4: Run Tests

```bash
make test
```

## Step 5: Lint and type-check before your PR

CI runs **`make test`** on push and pull requests. **Lint and mypy are not in CI yet**, so you should run them locally to avoid review round-trips:

```bash
make lint       # ruff
make typecheck  # mypy (targets Python 3.11 per pyproject.toml)
```

Optionally run `make format` to auto-format. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for the full workflow.
