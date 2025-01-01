# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

# Format the Just code
format:
    just --fmt --unstable

# Check for Just format issues
format-check:
    just --fmt --check --unstable
