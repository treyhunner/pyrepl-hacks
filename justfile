# Show available commands
_default:
    @just --list --unsorted

# Python Python package
build:
    uv build

# Publish to PyPI
publish:
    uv publish
