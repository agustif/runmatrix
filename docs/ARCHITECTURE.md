# Architecture

## Core principle

`runmatrix` is a DAG-first experiment runner.

It should be thought of as:

- a local execution kernel
- for CI-style job graphs
- with reusable loaders and runners

The stable abstraction is:

- **canonical manifest IR**
- **planner**
- **runtime kernel**
- **plugin boundaries**

Everything else is built around those seams.

## Layers

### 1. Domain

Pure types for:

- manifest
- tasks
- matrices
- dependency edges via `needs`
- plans
- task results
- execution modes

This layer has no I/O.

### 2. Planning

Transforms input IR into an executable DAG:

- inheritance
- matrix expansion
- dependency validation through `needs`
- topo planning

This layer should be deterministic.

### 3. Runtime

Executes a planned DAG:

- sequential
- bounded parallel

Later extensions can add:

- concurrency groups
- outputs
- conditional task skipping

This layer emits lifecycle events but should not know about specific sinks.

### 4. Plugins

Three main extension families:

- loaders
- runners
- hooks/sinks

### 5. CLI

Thin wrapper around planning and runtime.

## Canonical IR

All frontends should compile to the same internal model:

- `Manifest`
- `TaskSpec`
- `ExpandedTask`
- `Plan`

This is intentionally similar to the useful semantic layer of CI systems:

- workflows -> manifests
- jobs -> tasks
- `needs` -> DAG edges
- matrix -> expanded tasks

That keeps loaders replaceable.

## Out of scope

- hosted tracking
- distributed scheduling
- remote worker orchestration
- ML-specific semantics
- CI expression-language complexity
