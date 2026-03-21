"""Prompt compiler -- assembles a final prompt from components."""

from __future__ import annotations

from typing import Any

from agentguard.prompt_framework.linter import LintWarning, lint_prompt
from agentguard.prompt_framework.registry import PromptPackage


class CompiledPrompt:
    """The assembled prompt ready for LLM invocation."""

    __slots__ = ("messages", "output_schema", "tool_definitions", "lint_warnings", "metadata")

    def __init__(
        self,
        messages: list[dict[str, str]],
        output_schema: dict[str, Any] | None,
        tool_definitions: list[dict[str, Any]],
        lint_warnings: list[LintWarning],
        metadata: dict[str, Any],
    ):
        self.messages = messages
        self.output_schema = output_schema
        self.tool_definitions = tool_definitions
        self.lint_warnings = lint_warnings
        self.metadata = metadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "messages": self.messages,
            "output_schema": self.output_schema,
            "tool_definitions": self.tool_definitions,
            "lint_warnings": [w.to_dict() for w in self.lint_warnings],
            "metadata": self.metadata,
        }


def compile_prompt(
    package: PromptPackage,
    *,
    user_message: str,
    tenant_policy: str = "",
    retrieved_context: str = "",
    variables: dict[str, str] | None = None,
) -> CompiledPrompt:
    """Assemble a prompt from package definition + runtime inputs.

    Compilation order:
    1. System instructions (from package)
    2. Developer policy (from package)
    3. Tenant policy (runtime override)
    4. Grounding instructions + retrieved context
    5. Refusal policy
    6. Output schema instructions
    7. User message
    """
    vars_ = variables or {}

    system_parts: list[str] = []

    # 1. System instructions
    sys_inst = _interpolate(package.system_instructions, vars_)
    system_parts.append(sys_inst)

    # 2. Developer policy
    if package.developer_policy:
        system_parts.append(f"\n## Developer Policy\n{package.developer_policy}")

    # 3. Tenant policy
    if tenant_policy:
        system_parts.append(f"\n## Tenant Policy\n{tenant_policy}")

    # 4. Grounding
    if package.grounding_instructions:
        grounding = package.grounding_instructions
        if retrieved_context:
            grounding += f"\n\n### Retrieved Context\n{retrieved_context}"
        system_parts.append(f"\n## Grounding\n{grounding}")

    # 5. Refusal policy
    if package.refusal_policy:
        system_parts.append(f"\n## Refusal Policy\n{package.refusal_policy}")

    # 6. Output schema
    if package.output_schema:
        import json

        schema_str = json.dumps(package.output_schema, indent=2)
        system_parts.append(f"\n## Output Schema\nRespond in this JSON schema:\n```json\n{schema_str}\n```")

    system_content = "\n".join(system_parts)

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_message},
    ]

    warnings = lint_prompt(
        framework=package.framework,
        system_instructions=package.system_instructions,
        refusal_policy=package.refusal_policy,
        grounding_instructions=package.grounding_instructions,
        output_schema=package.output_schema,
        tool_definitions=package.tool_definitions or None,
    )

    return CompiledPrompt(
        messages=messages,
        output_schema=package.output_schema,
        tool_definitions=package.tool_definitions,
        lint_warnings=warnings,
        metadata={"package": package.name, "version": package.version},
    )


def _interpolate(template: str, variables: dict[str, str]) -> str:
    """Simple {{variable}} interpolation."""
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result
