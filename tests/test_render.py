from __future__ import annotations

from runmatrix.cli.render import render_dependency_tree, render_stage_table
from runmatrix.domain.plan import Plan, PlanStage
from runmatrix.domain.task import ExpandedTask


def test_render_stage_table_and_dependency_tree() -> None:
    plan = Plan(
        tasks=[
            ExpandedTask(id="base", base_id="base", command="echo base", env={}, needs=[]),
            ExpandedTask(
                id="sweep_001",
                base_id="sweep",
                command="echo run",
                env={},
                needs=["base"],
            ),
            ExpandedTask(
                id="sweep_002",
                base_id="sweep",
                command="echo run",
                env={},
                needs=["base"],
            ),
        ],
        stages=[
            PlanStage(index=0, task_ids=["base"]),
            PlanStage(index=1, task_ids=["sweep_001", "sweep_002"]),
        ],
    )

    table = render_stage_table(plan)
    tree = render_dependency_tree(plan)

    assert "stage" in table
    assert "base" in table
    assert "sweep_001" in table
    assert "DAG" not in table
    assert "base" in tree
    assert "sweep_001" in tree
    assert "├─" in tree or "└─" in tree
