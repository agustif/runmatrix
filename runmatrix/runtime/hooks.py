from __future__ import annotations

from typing import Protocol

from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask


class Hook(Protocol):
    def on_plan_built(self, plan: Plan) -> None: ...

    def before_task_run(self, task: ExpandedTask) -> None: ...

    def after_task_run(self, task: ExpandedTask, result: TaskResult) -> None: ...
