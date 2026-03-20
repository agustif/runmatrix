# CLI

The CLI is intentionally thin. It is a convenience layer over the planner and
runtime kernel, not the center of the system.

## Commands

### `inspect`

Build and render a manifest plan without executing it.

```bash
runmatrix inspect examples/basic.yaml
```

Output includes:

- stage table
- dependency tree

### `run`

Execute a manifest locally with the default shell runner and console hook.

```bash
runmatrix run examples/basic.yaml
```

or simply:

```bash
runmatrix examples/basic.yaml
```

The current vertical slice executes tasks sequentially in topological order.

In a real interactive terminal, the console sink shows an animated Rich status
spinner while each task is running, then prints a completion line with the
return code and elapsed time.

If the task emits stdout or stderr, the default console sink also renders those
streams in bordered output panels after completion, truncated to a reasonable
number of lines.

## Supported manifest extensions

- `.yaml`
- `.yml`
- `.json`
- `.toml`

## Current limitations

- no bounded parallel scheduler yet
- no event-file sink yet
- no resume/retry model yet
- no outputs or concurrency groups yet
