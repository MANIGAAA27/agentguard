"""Prompt framework API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.prompt_framework.compiler import compile_prompt
from agentguard.prompt_framework.registry import list_packages, load_prompt_package
from agentguard.prompt_framework.schemas import PromptCompileRequest, PromptCompileResponse

router = APIRouter(prefix="/v1/prompts", tags=["prompt-framework"])


@router.post(
    "/compile",
    response_model=PromptCompileResponse,
    summary="Compile a versioned prompt package into LLM-ready messages",
    description=(
        "Loads a prompt package by name/version, assembles system instructions, "
        "developer policy, tenant policy, grounding context, refusal policy, "
        "and output schema into a final message array. Runs lint checks for anti-patterns."
    ),
)
async def compile_prompt_endpoint(
    body: PromptCompileRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> PromptCompileResponse:
    try:
        package = load_prompt_package(body.package_name, body.package_version)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    compiled = compile_prompt(
        package,
        user_message=body.user_message,
        tenant_policy=body.tenant_policy,
        retrieved_context=body.retrieved_context,
        variables=body.variables,
    )
    data = compiled.to_dict()
    return PromptCompileResponse(correlation_id=ctx.correlation_id, **data)


@router.get("/packages", summary="List available prompt packages")
async def list_prompt_packages() -> list[dict[str, str]]:
    return list_packages()
