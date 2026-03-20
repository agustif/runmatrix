from __future__ import annotations

from pydantic import BaseModel

from .enums import TaskStatus


class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
