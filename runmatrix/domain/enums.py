from __future__ import annotations

from enum import StrEnum


class MatrixStrategy(StrEnum):
    PRODUCT = "product"
    ZIP = "zip"


class ExecutionMode(StrEnum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"
