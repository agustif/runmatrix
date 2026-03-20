from __future__ import annotations

from pydantic import BaseModel, Field

from .task import TaskSpec


class Manifest(BaseModel):
    """Canonical manifest IR.

    Frontend formats like YAML/JSON/TOML should all compile into this model.
    """

    runner: str | None = None
    extends: list[str] = Field(default_factory=list)
    defaults: dict[str, str] = Field(default_factory=dict)
    tasks: list[TaskSpec] = Field(default_factory=list)
