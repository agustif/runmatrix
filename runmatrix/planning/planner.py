from __future__ import annotations

from runmatrix.domain.manifest import Manifest
from runmatrix.domain.plan import Plan

from .expand import expand_task
from .stages import compute_stages
from .validate import validate_needs


def build_plan(manifest: Manifest) -> Plan:
    tasks = []
    for task in manifest.tasks:
        tasks.extend(expand_task(task, manifest.defaults))
    validate_needs(tasks)
    return Plan(tasks=tasks, stages=compute_stages(tasks))
