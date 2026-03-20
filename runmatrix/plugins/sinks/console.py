from __future__ import annotations

import time

from rich.console import Console
from rich.panel import Panel
from rich.status import Status

from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask


class ConsoleHook:
    def __init__(self, *, max_output_lines: int = 20) -> None:
        self.console = Console(highlight=False)
        self.max_output_lines = max_output_lines
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
        self._render_output(task.id, "stdout", result.stdout, border_style="blue")
        self._render_output(task.id, "stderr", result.stderr, border_style="yellow")

    def _render_output(
        self,
        task_id: str,
        stream_name: str,
        text: str,
        *,
        border_style: str,
    ) -> None:
        lines = [line.rstrip() for line in text.splitlines()]
        if not lines:
            return
        truncated = lines[: self.max_output_lines]
        if len(lines) > self.max_output_lines:
            truncated.append(f"... ({len(lines) - self.max_output_lines} more lines)")
        body = "\n".join(truncated)
        self.console.print(
            Panel(
                body,
                title=f"{task_id} {stream_name}",
                border_style=border_style,
                expand=False,
            )
        )
