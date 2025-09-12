# Contributing to pyrepl-hacks

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for dependency management
- [just](https://github.com/casey/just) for task running

## Getting Started

Install dependencies and pre-commit hooks:

```console
just setup
```

## Running Tests

Run tests on both Python 3.13 and 3.14 with coverage:

```console
just test
```

Run HTML code coverage report and open in a web browser:

```console
just test-html
```

## Code Quality

Run linting and auto-format code:

```console
just fmt
```

Run pre-commit hooks manually:

```console
just prek
```

### Tools Used

These tools will be auto-installed with uv as needed:

- [prek](https://github.com/j178/prek) for pre-commit hooks to lint & format code
- [ruff](https://docs.astral.sh/ruff/) for linting & auto-formatting Python code
- [rumdl](https://github.com/rvben/rumdl) for linting & auto-formatting markdown
- [coverage](https://coverage.readthedocs.io) for measuring code coverage
