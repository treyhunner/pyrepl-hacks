# Show available commands
_default:
    @just --list --unsorted

# Run the tests with coverage
test *args:
    uv run --group test coverage run -m unittest {{ args }}
    uv run --group test coverage report

# Run tests with coverage and generate HTML report
test-html *args:
    uv run --group test coverage run -m unittest {{ args }}
    uv run --group test coverage html
    @echo "Opening coverage report generated at htmlcov/index.html"
    uv run python -m webbrowser htmlcov/index.html


# Python Python package
build:
    uv build

# Publish to PyPI
publish:
    uv publish
