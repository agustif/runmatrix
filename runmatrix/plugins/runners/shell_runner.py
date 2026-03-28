from __future__ import annotations

import os
import shlex
import subprocess
import threading
from pathlib import Path
from shutil import which

from runmatrix.domain.enums import TaskStatus
from runmatrix.domain.result import TaskResult
from runmatrix.domain.task import ExpandedTask


class ShellRunner:
    def run(self, task: ExpandedTask, cwd: Path, hooks) -> TaskResult:
        env = dict(os.environ)
        env.update(task.env)
        command = task.command
        use_stdbuf = os.environ.get("RUNMATRIX_DISABLE_STDBUF", "0") != "1" and which("stdbuf")
        if use_stdbuf:
            command = f"stdbuf -oL -eL bash -lc {shlex.quote(command)}"
        proc = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        def stream_output(pipe, stream_name: str, sink: list[str]) -> None:
            if pipe is None:
                return
            for line in iter(pipe.readline, ""):
                stripped = line.rstrip("\n")
                sink.append(stripped)
                for hook in hooks:
                    hook.on_task_output(task, stream_name, stripped)
            pipe.close()

        threads = [
            threading.Thread(target=stream_output, args=(proc.stdout, "stdout", stdout_lines)),
            threading.Thread(target=stream_output, args=(proc.stderr, "stderr", stderr_lines)),
        ]
        for thread in threads:
            thread.start()

        returncode = proc.wait()
        for thread in threads:
            thread.join()

        return TaskResult(
            task_id=task.id,
            status=TaskStatus.SUCCEEDED if returncode == 0 else TaskStatus.FAILED,
            returncode=returncode,
            stdout="\n".join(stdout_lines),
            stderr="\n".join(stderr_lines),
        )
