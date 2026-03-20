# Plugins

`runmatrix` is intended to stay small by pushing I/O and integrations into
plugins.

## Plugin families

### Loaders

- YAML
- JSON
- TOML

These convert source files into the canonical manifest IR.

### Runners

Current:

- shell runner

Future:

- python callable runner
- container runner
- remote/SSH runner

### Hooks / sinks

Current:

- console sink

Future:

- JSONL event sink
- analytics sink
- notifications

## Design rule

If a feature can be expressed as a hook or plugin, it should not live in the
execution kernel.
