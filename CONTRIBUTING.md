# Contributing

Thanks for contributing to `runmatrix`.

This project is intentionally narrow:

- DAG-first planning
- local execution
- hooks/plugins
- terminal-native UX

Please keep changes aligned with that scope.

## Development setup

```bash
git clone https://github.com/agustif/runmatrix.git
cd runmatrix
uv sync
```

## Common commands

Run checks:

```bash
uv run ruff check runmatrix tests
uv run ty check
uv run pytest
```

Build distributions:

```bash
uv build
```

Try the example:

```bash
uv run python -m runmatrix.cli.main inspect examples/basic.yaml
uv run python -m runmatrix.cli.main examples/basic.yaml
```

## Project structure

- `runmatrix/domain/`
  - typed canonical IR
- `runmatrix/planning/`
  - expansion, validation, stage planning
- `runmatrix/runtime/`
  - execution kernel and hook contracts
- `runmatrix/plugins/`
  - loaders, runners, sinks
- `runmatrix/cli/`
  - thin CLI/TUI surfaces
- `docs/`
  - system documentation
- `examples/`
  - runnable manifests
- `tests/`
  - automated coverage

## Design guidelines

- Keep the core small and explicit.
- Prefer typed contracts over magic behavior.
- If a feature can live in a hook or plugin, keep it out of the kernel.
- Borrow good CI semantics:
  - `tasks`
  - `needs`
  - `matrix`
  - reusable defaults
- Do not copy CI syntax complexity or expression languages.

## UX guidelines

- Treat terminal UX as a real product surface.
- Prefer dense, quiet, scan-friendly output.
- Keep hierarchy clear and decoration restrained.
- Show real task output, not just status.

## Docs guidelines

If behavior changes, update the relevant docs in the same PR:

- `README.md` for user-facing behavior
- `docs/CLI.md` for CLI changes
- `docs/MANIFESTS.md` for manifest semantics
- examples when syntax or behavior changes

## Release guidelines

- GitHub release + PyPI trusted publishing is the preferred release path.
- Keep automation minimal and auditable.
- Verify `uv build` locally before touching release automation.
