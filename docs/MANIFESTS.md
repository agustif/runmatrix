# Manifests

`runmatrix` supports manifests in:

- YAML
- JSON
- TOML

All loaders compile into the same canonical `Manifest` model.

## Core fields

- `defaults`
- `tasks`

Each task can declare:

- `id`
- `command`
- `env`
- `needs`
- `matrix`

## Matrix

Current strategies:

- `product`
- `zip`

Example:

```yaml
tasks:
  - id: sweep
    command: echo sweep
    matrix:
      strategy: zip
      name_prefix: sweep
      params:
        RUN_ID: [a, b]
        WIDTH: ["256", "384"]
```

This expands into:

- `sweep_001`
- `sweep_002`

## Future

The intended next step is manifest inheritance and reusable defaults.
