from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DrillInputs(BaseModel):
    """Typed, validated input boundary for drills.

    Intended sources:
    - GitHub Actions workflow_dispatch inputs
    - environment variables
    - CLI flags

    Scenario-specific inputs can be passed as extra fields; each scenario handler
    may define its own more specific InputModel later.
    """

    model_config = ConfigDict(extra="allow")

    scenario: str = Field(..., description="Scenario key (registry name)")
    scope_id: str = Field(..., description="Evidence scope folder, e.g. S2B-2A-1A")
    run_id: str = Field(..., description="Run id used in evidence bundle paths")

    # Optional operational knobs common to many scenarios
    timeout_s: int | None = Field(default=None, ge=1)
    sampling: float | None = Field(default=None, ge=0.0, le=1.0)


class DrillResult(BaseModel):
    """Minimal contract that can be serialized into _result.json."""

    ok: bool
    meta: dict[str, Any] = Field(default_factory=dict)
    summary: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
