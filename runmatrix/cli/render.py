from __future__ import annotations

from shutil import get_terminal_size

from runmatrix.domain.plan import Plan


def _truncate(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    if width <= 1:
        return text[:width]
    return text[: width - 1] + "…"


def render_stage_table(plan: Plan) -> str:
    width = get_terminal_size((100, 24)).columns
    stage_col = 8
    count_col = 7
    tasks_col = max(width - stage_col - count_col - 6, 20)
    lines = []
    header = f"{'stage':<{stage_col}}  {'count':<{count_col}}  {'tasks':<{tasks_col}}"
    rule = f"{'─' * stage_col}  {'─' * count_col}  {'─' * tasks_col}"
    lines.extend([header, rule])
    for stage in plan.stages:
        tasks = ", ".join(stage.task_ids)
        row = (
            f"{str(stage.index):<{stage_col}}  "
            f"{str(len(stage.task_ids)):<{count_col}}  "
            f"{_truncate(tasks, tasks_col)}"
        )
        lines.append(
            row
        )
    return "\n".join(lines)


def render_dependency_tree(plan: Plan) -> str:
    dependents: dict[str, list[str]] = {task.id: [] for task in plan.tasks}
    roots: list[str] = []
    ids_by_base: dict[str, list[str]] = {}
    for task in plan.tasks:
        ids_by_base.setdefault(task.base_id, []).append(task.id)

    for task in plan.tasks:
        expanded_needs: list[str] = []
        for need in task.needs:
            expanded_needs.extend(ids_by_base.get(need, [need]))
        if not expanded_needs:
            roots.append(task.id)
        for dep in expanded_needs:
            if dep in dependents:
                dependents[dep].append(task.id)

    lines: list[str] = []

    def walk(node: str, prefix: str, is_last: bool) -> None:
        connector = "└─" if is_last else "├─"
        lines.append(f"{prefix}{connector} {node}")
        children = sorted(dependents.get(node, []))
        next_prefix = prefix + ("   " if is_last else "│  ")
        for idx, child in enumerate(children):
            walk(child, next_prefix, idx == len(children) - 1)

    sorted_roots = sorted(set(roots))
    for idx, root in enumerate(sorted_roots):
        walk(root, "", idx == len(sorted_roots) - 1)

    return "\n".join(lines)
