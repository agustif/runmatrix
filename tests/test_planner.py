from __future__ import annotations

from runmatrix.domain.manifest import Manifest
from runmatrix.domain.task import MatrixSpec, TaskSpec
from runmatrix.planning.planner import build_plan


def test_build_plan_expands_matrix_tasks() -> None:
    manifest = Manifest(
        defaults={"PROFILE": "smoke"},
        tasks=[
            TaskSpec(id="base", command="echo base"),
            TaskSpec(
                id="sweep",
                command="echo run",
                needs=["base"],
                matrix=MatrixSpec(
                    strategy="zip",
                    name_prefix="sweep",
                    params={"RUN_ID": ["a", "b"], "WIDTH": ["256", "384"]},
                ),
            ),
        ],
    )

    plan = build_plan(manifest)

    assert [task.id for task in plan.tasks] == ["base", "sweep_001", "sweep_002"]
    assert plan.tasks[1].needs == ["base"]
    assert plan.tasks[1].env["RUN_ID"] == "a"
    assert plan.tasks[2].env["WIDTH"] == "384"
    assert [stage.task_ids for stage in plan.stages] == [["base"], ["sweep_001", "sweep_002"]]
