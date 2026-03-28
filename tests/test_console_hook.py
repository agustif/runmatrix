from __future__ import annotations

from runmatrix.domain.enums import TaskStatus
from runmatrix.domain.plan import Plan
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask
from runmatrix.plugins.sinks.console import ConsoleHook


def test_console_hook_tracks_status_lifecycle() -> None:
    hook = ConsoleHook(live_output_mode="prefixed")
    task = ExpandedTask(id="task", base_id="task", command="echo hi", env={}, needs=[])
    result = TaskResult(task_id="task", status=TaskStatus.SUCCEEDED, returncode=0)

    hook.on_plan_built(Plan(tasks=[task]))
    hook.before_task_run(task)
    assert hook._status is not None
    hook.after_task_run(task, result)
    assert hook._status is None


def test_console_hook_raw_output_skips_status() -> None:
    hook = ConsoleHook(live_output_mode="raw")
    task = ExpandedTask(id="task", base_id="task", command="echo hi", env={}, needs=[])
    result = TaskResult(task_id="task", status=TaskStatus.SUCCEEDED, returncode=0)

    hook.before_task_run(task)
    assert hook._status is None
    hook.after_task_run(task, result)
    assert hook._status is None


def test_console_hook_renders_output_without_crashing() -> None:
    hook = ConsoleHook(max_output_lines=2)
    task = ExpandedTask(id="task", base_id="task", command="echo hi", env={}, needs=[])
    result = TaskResult(
        task_id="task",
        status=TaskStatus.SUCCEEDED,
        returncode=0,
        stdout="line1\nline2\nline3",
        stderr="warn1\nwarn2\nwarn3",
    )

    hook.before_task_run(task)
    hook.after_task_run(task, result)

    assert hook._status is None
