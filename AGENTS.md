# AGENTS.md for `runmatrix`

This file governs the entire `/Users/af/runmatrix` repository.

## Purpose

`runmatrix` is a narrow reusable library for:

- manifest loading
- DAG planning
- local execution
- hooks/plugins
- terminal-native operator UX

Do not grow it into a hosted platform, experiment database, or ML-specific
framework inside this repo.

## Design rules

- Keep the core small: domain, planning, runtime, plugins, CLI.
- Prefer explicit typed contracts over convenience magic.
- If a feature can live in a hook or plugin, keep it out of the runtime kernel.
- Treat CI-style semantics as the reference model:
  - `tasks`
  - `needs`
  - `matrix`
  - reusable defaults
- Do not clone GitHub Actions syntax or expression complexity.

## UX rules

- Terminal UX should be dense, quiet, and scan-friendly.
- Prefer clear hierarchy and alignment over decorative borders.
- Show real command output for executed tasks.
- Default CLI behavior should be obvious:
  - `runmatrix file.yaml` runs
  - `runmatrix inspect file.yaml` inspects

## Dependency rules

- Reuse well-supported dependencies where they remove real complexity.
- Current preferred stack:
  - `pydantic`
  - `PyYAML`
  - stdlib `json`
  - stdlib `tomllib`
  - `rich`
  - `textual`
  - `pytest`
  - `ruff`
  - `ty`
- Avoid adding heavy dependencies unless they clearly simplify the core.

## Testing and validation

Before considering work complete, run:

```bash
uv run ruff check runmatrix tests
uv run ty check
uv run pytest
```

If packaging or release logic changed, also run:

```bash
uv build
```

## Docs rules

- Keep `README.md` user-facing and concise.
- Put deeper system details in `docs/`.
- If CLI behavior changes, update both:
  - `README.md`
  - `docs/CLI.md`
- If manifest semantics change, update:
  - `docs/MANIFESTS.md`
  - examples

## Release rules

- Prefer GitHub release + PyPI trusted publishing.
- Keep release automation minimal and auditable.
- Do not document source-checkout behavior as if it were the primary install path.
- Prefer installed `runmatrix` usage in docs; mention `uvx` only as a lightweight try-it path.
