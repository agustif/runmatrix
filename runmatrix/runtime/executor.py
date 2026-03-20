from __future__ import annotations

from pathlib import Path

from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.runtime.hooks import Hook


def run_plan(
    plan: Plan,
    *,
    cwd: Path,
    runner,
    hooks: list[Hook],
) -> list[TaskResult]:
    for hook in hooks:
        hook.on_plan_built(plan)
    results: list[TaskResult] = []
    for task in plan.tasks:
        for hook in hooks:
            hook.before_task_run(task)
        result = runner.run(task, cwd)
        results.append(result)
        for hook in hooks:
            hook.after_task_run(task, result)
    return results
