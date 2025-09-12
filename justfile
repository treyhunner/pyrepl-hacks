# Show available commands
_default:
    @just --list --unsorted

# Run the tests with coverage on both Python versions
test *args:
    uv run --python 3.13 --group test coverage run -m unittest {{ args }}
    uv run --python 3.14 --group test coverage run --append -m unittest {{ args }}
    uv run --group test coverage report

# Run tests with coverage and generate HTML report
test-html *args:
    uv run --python 3.13 --group test coverage run -m unittest {{ args }}
    uv run --python 3.14 --group test coverage run --append -m unittest {{ args }}
    uv run --group test coverage html
    @echo "Opening coverage report generated at htmlcov/index.html"
    uv run python -m webbrowser htmlcov/index.html

# Format code with ruff
fmt:
    uv run --group lint ruff check --fix
    uv run --group lint ruff format

# Run all quality checks (format, lint, test)
check:
    just fmt
    just lint
    just test

# Install prek git hooks
install-hooks:
    uv run --group dev prek install

# Run prek hooks manually
run-hooks:
    uv run --group dev prek run


# Python Python package
build:
    uv build

# Publish to PyPI
publish:
    uv publish
