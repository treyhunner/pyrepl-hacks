# Show available commands
_default:
    @just --list --unsorted

# Install prek git hooks
setup:
    # https://github.com/astral-sh/uv/issues/7655#issuecomment-2600986729
    UV_VENV_SEED=1 uv venv
    uv sync --all-groups
    uv run --group dev prek install

# Run prek hooks manually
prek:
    uv run --group dev prek run

# Run the tests on both Python versions
test *args:
    #!/usr/bin/env bash
    if [[ -n "{{ args }}" ]]; then
        # Run without coverage
        uv run --python 3.13 --group test python -m unittest {{ args }}
        uv run --python 3.14 --group test python -m unittest {{ args }}
    else
        # Run with coverage
        uv run --python 3.13 --group test coverage run -m unittest {{ args }}
        uv run --python 3.14 --group test coverage run --append -m unittest {{ args }}
        uv run --group test coverage report
    fi

# Run tests with coverage and generate HTML report
test-html *args:
    uv run --python 3.13 --group test coverage run -m unittest {{ args }}
    uv run --python 3.14 --group test coverage run --append -m unittest {{ args }}
    uv run --group test coverage html
    @echo "Opening coverage report generated at htmlcov/index.html"
    uv run python -m webbrowser htmlcov/index.html

# Format code with ruff, markdown with rumdl, and type check
fmt:
    uv run --group lint ruff check --fix
    uv run --group lint ruff format
    uv run --group lint rumdl fmt --fix
    uv run --group typecheck mypy --strict pyrepl_hacks

# Run all quality checks, auto-formatting, and run tests
check:
    just fmt
    just test

# Bump version
bump value:
    uv version --bump {{ value }}

# Python Python package
build:
    uv sync  # Force uv version error if applicable
    uv build --clear

# Publish to PyPI
publish:
    uv publish
