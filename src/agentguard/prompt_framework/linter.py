"""Prompt anti-pattern detection and linting."""

from __future__ import annotations

from agentguard.prompt_framework.frameworks import FRAMEWORK_SPECS, FrameworkType


class LintWarning:
    __slots__ = ("code", "message", "severity")

    def __init__(self, code: str, message: str, severity: str = "warning"):
        self.code = code
        self.message = message
        self.severity = severity

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "severity": self.severity}


def lint_prompt(
    *,
    framework: str,
    system_instructions: str,
    refusal_policy: str,
    grounding_instructions: str,
    output_schema: dict | None,
    tool_definitions: list | None,
) -> list[LintWarning]:
    """Detect anti-patterns in a prompt configuration. Returns a list of warnings."""
    warnings: list[LintWarning] = []

    try:
        fw_type = FrameworkType(framework)
    except ValueError:
        warnings.append(LintWarning("UNKNOWN_FRAMEWORK", f"Unknown framework: {framework}", "error"))
        return warnings

    spec = FRAMEWORK_SPECS[fw_type]

    if spec.requires_role_definition and len(system_instructions.strip()) < 20:
        warnings.append(LintWarning(
            "VAGUE_ROLE",
            "System instructions are too short; provide a clear role definition",
        ))

    if spec.requires_refusal_policy and not refusal_policy.strip():
        warnings.append(LintWarning(
            "NO_REFUSAL_POLICY",
            "No refusal policy defined; the model may answer unsafe questions",
            "error",
        ))

    if spec.requires_grounding and not grounding_instructions.strip():
        warnings.append(LintWarning(
            "NO_GROUNDING",
            "Framework requires grounding but no grounding instructions provided",
            "error",
        ))

    if spec.requires_output_schema and not output_schema:
        warnings.append(LintWarning(
            "MISSING_OUTPUT_SCHEMA",
            "Framework requires an output schema but none provided",
            "error",
        ))

    if spec.requires_tool_definitions and not tool_definitions:
        warnings.append(LintWarning(
            "UNRESTRICTED_TOOL_ACCESS",
            "Framework requires tool definitions but none provided; tools are unrestricted",
            "error",
        ))

    return warnings
