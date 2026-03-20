from __future__ import annotations

import argparse
from pathlib import Path

from runmatrix.cli.render import render_dependency_tree, render_stage_table
from runmatrix.planning.planner import build_plan
from runmatrix.plugins.loaders.json_loader import load_json_manifest
from runmatrix.plugins.loaders.toml_loader import load_toml_manifest
from runmatrix.plugins.loaders.yaml_loader import load_yaml_manifest
from runmatrix.plugins.runners.shell_runner import ShellRunner
from runmatrix.plugins.sinks.console import ConsoleHook
from runmatrix.runtime.executor import run_plan


def _load_manifest(path: Path):
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return load_yaml_manifest(path)
    if suffix == ".json":
        return load_json_manifest(path)
    if suffix == ".toml":
        return load_toml_manifest(path)
    raise ValueError(f"Unsupported manifest file extension: {path.suffix}")


def cmd_plan(path: Path) -> None:
    manifest = _load_manifest(path)
    plan = build_plan(manifest)
    print(render_stage_table(plan))
    print()
    print("DAG")
    print(render_dependency_tree(plan))


def cmd_run(path: Path) -> None:
    manifest = _load_manifest(path)
    plan = build_plan(manifest)
    run_plan(plan, cwd=path.parent, runner=ShellRunner(), hooks=[ConsoleHook()])


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("manifest", type=Path)

    run = sub.add_parser("run")
    run.add_argument("manifest", type=Path)

    args = parser.parse_args()
    if args.command == "plan":
        cmd_plan(args.manifest)
    elif args.command == "run":
        cmd_run(args.manifest)


if __name__ == "__main__":
    main()
