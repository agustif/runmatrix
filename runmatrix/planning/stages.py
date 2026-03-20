from __future__ import annotations

from collections import defaultdict, deque

from runmatrix.domain.plan import PlanStage
from runmatrix.domain.task import ExpandedTask


def compute_stages(tasks: list[ExpandedTask]) -> list[PlanStage]:
    task_by_id = {task.id: task for task in tasks}
    base_id_to_task_ids: dict[str, list[str]] = defaultdict(list)
    for task in tasks:
        base_id_to_task_ids[task.base_id].append(task.id)

    indegree = {task.id: 0 for task in tasks}
    adjacency: dict[str, list[str]] = defaultdict(list)

    for task in tasks:
        expanded_needs: list[str] = []
        for need in task.needs:
            if need in base_id_to_task_ids:
                expanded_needs.extend(base_id_to_task_ids[need])
            elif need in task_by_id:
                expanded_needs.append(need)
        for dep in expanded_needs:
            adjacency[dep].append(task.id)
            indegree[task.id] += 1

    stages: list[PlanStage] = []
    ready = deque(sorted(task_id for task_id, degree in indegree.items() if degree == 0))
    visited = 0

    while ready:
        current = list(ready)
        ready.clear()
        stages.append(PlanStage(index=len(stages), task_ids=current))
        for task_id in current:
            visited += 1
            for nxt in adjacency[task_id]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    ready.append(nxt)
        ready = deque(sorted(ready))

    if visited != len(tasks):
        raise ValueError("Task graph contains a cycle")

    return stages
