from __future__ import annotations

import itertools

from runmatrix.domain.enums import MatrixStrategy
from runmatrix.domain.task import ExpandedTask, MatrixParamSpec, TaskSpec


def _expand_matrix_param(spec: list[str] | MatrixParamSpec) -> list[str]:
    if isinstance(spec, list):
        return spec
    if spec.values is not None:
        return spec.values
    if spec.range is not None:
        return [str(x) for x in range(spec.range.start, spec.range.stop, spec.range.step)]
    raise ValueError("Matrix parameter spec must define values or range")


def expand_task(task: TaskSpec, defaults: dict[str, str]) -> list[ExpandedTask]:
    base_env = dict(defaults)
    base_env.update(task.env)
    if task.matrix is None:
        return [
            ExpandedTask(
                id=task.id,
                base_id=task.id,
                command=task.command,
                env=base_env,
                needs=task.needs,
                outputs=task.outputs,
                concurrency_group=task.concurrency_group,
            )
        ]

    params = {key: _expand_matrix_param(spec) for key, spec in task.matrix.params.items()}
    if task.matrix.strategy == MatrixStrategy.PRODUCT:
        keys = list(params)
        rows = [
            dict(zip(keys, combo, strict=True))
            for combo in itertools.product(*(params[key] for key in keys))
        ]
    elif task.matrix.strategy == MatrixStrategy.ZIP:
        lengths = {len(values) for values in params.values()}
        if len(lengths) != 1:
            raise ValueError("Zip matrix requires equal-length parameter lists")
        keys = list(params)
        rows = [{key: params[key][i] for key in keys} for i in range(next(iter(lengths)))]
    else:
        raise ValueError(f"Unsupported matrix strategy: {task.matrix.strategy}")

    expanded: list[ExpandedTask] = []
    for idx, row in enumerate(rows, start=1):
        env = dict(base_env)
        env.update(row)
        task_id = (
            f"{task.matrix.name_prefix}_{idx:03d}"
            if task.matrix.name_prefix
            else f"{task.id}_{idx:03d}"
        )
        expanded.append(
            ExpandedTask(
                id=task_id,
                base_id=task.id,
                command=task.command,
                env=env,
                needs=task.needs,
                outputs=task.outputs,
                concurrency_group=task.concurrency_group,
            )
        )
    return expanded
