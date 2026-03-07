"""Tests for prompt anti-pattern linting."""

from __future__ import annotations

from agentguard.prompt_framework.linter import lint_prompt


def test_rag_qa_no_grounding_warns():
    warnings = lint_prompt(
        framework="RAG_QA",
        system_instructions="You are a helpful assistant for answering questions.",
        refusal_policy="Refuse if no context.",
        grounding_instructions="",
        output_schema=None,
        tool_definitions=None,
    )
    codes = [w.code for w in warnings]
    assert "NO_GROUNDING" in codes


def test_tool_use_no_tools_warns():
    warnings = lint_prompt(
        framework="TOOL_USE",
        system_instructions="You are a tool-using assistant that helps users.",
        refusal_policy="Refuse unsafe requests.",
        grounding_instructions="",
        output_schema={"type": "object"},
        tool_definitions=None,
    )
    codes = [w.code for w in warnings]
    assert "UNRESTRICTED_TOOL_ACCESS" in codes


def test_vague_role_warns():
    warnings = lint_prompt(
        framework="CLASSIFICATION",
        system_instructions="Hi",
        refusal_policy="Refuse bad stuff.",
        grounding_instructions="",
        output_schema={"type": "object"},
        tool_definitions=None,
    )
    codes = [w.code for w in warnings]
    assert "VAGUE_ROLE" in codes


def test_no_refusal_policy_warns():
    warnings = lint_prompt(
        framework="RAG_QA",
        system_instructions="You are a helpful assistant for answering questions.",
        refusal_policy="",
        grounding_instructions="Use context.",
        output_schema=None,
        tool_definitions=None,
    )
    codes = [w.code for w in warnings]
    assert "NO_REFUSAL_POLICY" in codes


def test_clean_rag_qa():
    warnings = lint_prompt(
        framework="RAG_QA",
        system_instructions="You are a knowledgeable assistant that answers questions using context.",
        refusal_policy="Refuse if no context available.",
        grounding_instructions="Use only the provided context.",
        output_schema=None,
        tool_definitions=None,
    )
    error_warnings = [w for w in warnings if w.severity == "error"]
    assert len(error_warnings) == 0
