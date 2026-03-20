from __future__ import annotations

from rich.console import Console

from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask


class ConsoleHook:
    def __init__(self) -> None:
        self.console = Console(highlight=False)

    def on_plan_built(self, plan: Plan) -> None:
        self.console.print(f"[bold]plan[/bold] tasks={len(plan.tasks)}")

    def before_task_run(self, task: ExpandedTask) -> None:
        self.console.print(f"[cyan]run[/cyan] {task.id}")

    def after_task_run(self, task: ExpandedTask, result: TaskResult) -> None:
        style = "green" if result.returncode == 0 else "red"
        self.console.print(f"[{style}]done[/{style}] {task.id} rc={result.returncode}")
