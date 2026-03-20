from __future__ import annotations

from runmatrix.domain.enums import TaskStatus
from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask
from runmatrix.plugins.sinks.console import ConsoleHook


def test_console_hook_tracks_status_lifecycle() -> None:
    hook = ConsoleHook()
    task = ExpandedTask(id="task", base_id="task", command="echo hi", env={}, needs=[])
    result = TaskResult(task_id="task", status=TaskStatus.SUCCEEDED, returncode=0)

    hook.on_plan_built(Plan(tasks=[task]))
    hook.before_task_run(task)
    assert hook._status is not None
    hook.after_task_run(task, result)
    assert hook._status is None
