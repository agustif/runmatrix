from __future__ import annotations

import os
import subprocess
from pathlib import Path

from runmatrix.domain.enums import TaskStatus
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask


class ShellRunner:
    def run(self, task: ExpandedTask, cwd: Path) -> TaskResult:
        env = dict(os.environ)
        env.update(task.env)
        proc = subprocess.run(
            task.command,
            shell=True,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
        )
        return TaskResult(
            task_id=task.id,
            status=TaskStatus.SUCCEEDED if proc.returncode == 0 else TaskStatus.FAILED,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
