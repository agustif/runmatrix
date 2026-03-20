from __future__ import annotations

from pydantic import BaseModel, Field

from .task import ExpandedTask


class PlanStage(BaseModel):
    index: int
    task_ids: list[str] = Field(default_factory=list)


class Plan(BaseModel):
    tasks: list[ExpandedTask] = Field(default_factory=list)
    stages: list[PlanStage] = Field(default_factory=list)
