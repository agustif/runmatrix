from __future__ import annotations

import argparse
import os
import sys
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


def cmd_inspect(path: Path) -> None:
    manifest = _load_manifest(path)
    plan = build_plan(manifest)
    print(render_stage_table(plan))
    print()
    print("DAG")
    print(render_dependency_tree(plan))


def cmd_run(path: Path) -> None:
    manifest = _load_manifest(path)
    plan = build_plan(manifest)
    live_output = os.environ.get("RUNMATRIX_LIVE_OUTPUT", "raw").lower()
    if live_output == "off":
        hook = ConsoleHook(live_output=False)
    elif live_output in {"raw", "prefixed"}:
        hook = ConsoleHook(live_output=True, live_output_mode=live_output)
    else:
        raise ValueError("RUNMATRIX_LIVE_OUTPUT must be raw, prefixed, or off")
    run_plan(plan, cwd=path.parent, runner=ShellRunner(), hooks=[hook])


def main() -> None:
    is_manifest_path = (
        len(sys.argv) >= 2
        and not sys.argv[1].startswith("-")
        and Path(sys.argv[1]).suffix.lower() in {".yaml", ".yml", ".json", ".toml"}
    )
    if is_manifest_path:
        cmd_run(Path(sys.argv[1]))
        return

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("manifest", type=Path)

    run = sub.add_parser("run")
    run.add_argument("manifest", type=Path)

    args = parser.parse_args()
    if args.command == "inspect":
        cmd_inspect(args.manifest)
    elif args.command == "run":
        cmd_run(args.manifest)


if __name__ == "__main__":
    main()
