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

Run linting, auto-format code, and type checking:

```console
just fmt
```

Run all quality checks and tests:

```console
just check
```

Run pre-commit hooks manually:

```console
just prek
```


## Tools Used

These tools will be auto-installed with uv as needed:

- [prek](https://github.com/j178/prek) for pre-commit hooks to lint & format code
- [ruff](https://docs.astral.sh/ruff/) for linting & auto-formatting Python code
- [rumdl](https://github.com/rvben/rumdl) for linting & auto-formatting markdown
- [mypy](https://mypy-lang.org/) for static type checking
- [coverage](https://coverage.readthedocs.io) for measuring code coverage


## Development Workflow

The typical development workflow is:

1. Make your changes
2. Run `just fmt` to format, lint, and type check
3. Run `just test` to ensure tests pass (or run `just check` to `fmt` and `test` at once)
4. Commit (pre-commit hooks will run automatically)
