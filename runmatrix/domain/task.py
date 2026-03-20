from __future__ import annotations

from pydantic import BaseModel, Field


class MatrixRange(BaseModel):
    start: int
    stop: int
    step: int = 1


class MatrixParamSpec(BaseModel):
    values: list[str] | None = None
    range: MatrixRange | None = None


class MatrixSpec(BaseModel):
    strategy: str = "product"
    name_prefix: str | None = None
    params: dict[str, list[str] | MatrixParamSpec]


class TaskSpec(BaseModel):
    """Canonical task/job declaration.

    This is intentionally close to CI job semantics:

    - `id`: stable task identifier
    - `needs`: upstream task ids
    - `matrix`: optional expansion into multiple concrete tasks
    """

    id: str
    command: str
    env: dict[str, str] = Field(default_factory=dict)
    needs: list[str] = Field(default_factory=list)
    matrix: MatrixSpec | None = None
    outputs: dict[str, str] = Field(default_factory=dict)
    concurrency_group: str | None = None


class ExpandedTask(BaseModel):
    id: str
    base_id: str
    command: str
    env: dict[str, str]
    needs: list[str]
    outputs: dict[str, str] = Field(default_factory=dict)
    concurrency_group: str | None = None
