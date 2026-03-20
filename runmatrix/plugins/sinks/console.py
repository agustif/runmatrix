from __future__ import annotations

import time

from rich.console import Console
from rich.status import Status

from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask


class ConsoleHook:
    def __init__(self) -> None:
        self.console = Console(highlight=False)
        self._status: Status | None = None
        self._started_at: float | None = None

    def on_plan_built(self, plan: Plan) -> None:
        self.console.print(f"[bold]plan[/bold] tasks={len(plan.tasks)}")

    def before_task_run(self, task: ExpandedTask) -> None:
        self._started_at = time.perf_counter()
        self._status = self.console.status(f"[cyan]running[/cyan] {task.id}", spinner="dots")
        self._status.start()

    def after_task_run(self, task: ExpandedTask, result: TaskResult) -> None:
        elapsed = time.perf_counter() - self._started_at if self._started_at is not None else None
        if self._status is not None:
            self._status.stop()
            self._status = None
        self._started_at = None
        style = "green" if result.returncode == 0 else "red"
        elapsed_suffix = f" elapsed={elapsed:.2f}s" if elapsed is not None else ""
        self.console.print(
            f"[{style}]done[/{style}] {task.id} rc={result.returncode}{elapsed_suffix}"
        )
