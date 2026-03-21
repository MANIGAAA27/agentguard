"""Versioned prompt package registry -- loads YAML definitions from disk."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from agentguard.config import settings


class PromptPackage(BaseModel):
    """A versioned prompt package definition."""

    name: str
    version: str
    framework: str
    system_instructions: str
    developer_policy: str = ""
    refusal_policy: str = ""
    grounding_instructions: str = ""
    output_schema: dict[str, Any] | None = None
    tool_definitions: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


_cache: dict[str, PromptPackage] = {}


def load_prompt_package(name: str, version: str | None = None) -> PromptPackage:
    """Load a prompt package by name and optional version from the packages directory."""
    cache_key = f"{name}:{version or 'latest'}"
    if cache_key in _cache:
        return _cache[cache_key]

    pkg_dir = Path(settings.prompt_packages_dir) / name
    if not pkg_dir.is_dir():
        raise FileNotFoundError(f"Prompt package not found: {name}")

    if version:
        pkg_file = pkg_dir / f"{version}.yaml"
    else:
        yamls = sorted(pkg_dir.glob("*.yaml"), reverse=True)
        if not yamls:
            raise FileNotFoundError(f"No versions found for prompt package: {name}")
        pkg_file = yamls[0]

    with open(pkg_file) as f:
        data = yaml.safe_load(f)

    package = PromptPackage(**data)
    _cache[cache_key] = package
    return package


def list_packages() -> list[dict[str, str]]:
    """List all available prompt packages with their latest versions."""
    pkg_dir = Path(settings.prompt_packages_dir)
    result = []
    if pkg_dir.is_dir():
        for sub in sorted(pkg_dir.iterdir()):
            if sub.is_dir():
                yamls = sorted(sub.glob("*.yaml"), reverse=True)
                latest = yamls[0].stem if yamls else "none"
                result.append({"name": sub.name, "latest_version": latest})
    return result
