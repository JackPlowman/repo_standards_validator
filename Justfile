# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    poetry install

# Run the validator
run:
    poetry run python -m validator

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formatting
# Set up ruff red-knot when it's ready
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just ruff-format-fix
    just ruff-lint-fix

# Check for Ruff issues
ruff-lint-check:
    poetry run ruff check .

# Fix Ruff lint issues
ruff-lint-fix:
    poetry run ruff check . --fix

# Check for Ruff format issues
ruff-format-check:
    poetry run ruff format --check .

# Fix Ruff format issues
ruff-format-fix:
    poetry run ruff format .

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

# Check for unused code
vulture:
    poetry run vulture validator

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

# Format the Just code
format:
    just --fmt --unstable

# Check for Just format issues
format-check:
    just --fmt --check --unstable
