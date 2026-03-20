from __future__ import annotations

from runmatrix.domain.task import ExpandedTask


def validate_needs(tasks: list[ExpandedTask]) -> None:
    ids = {task.base_id for task in tasks} | {task.id for task in tasks}
    for task in tasks:
        for dep in task.needs:
            if dep not in ids:
                raise ValueError(f"Task {task.id} needs unknown dependency {dep}")
