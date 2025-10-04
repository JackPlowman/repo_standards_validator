# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install all python dependencies (including dev dependencies)
install:
    uv sync --extra dev

# Run the validator
run:
    uv run python -m validator

# ------------------------------------------------------------------------------
# Test Commands
# ------------------------------------------------------------------------------

# Run unit tests
unit-test: clean-repos
    uv run pytest validator --cov=. --cov-report=xml

# Run unit tests with debug output
unit-test-debug: clean-repos
    uv run pytest validator --cov=. --cov-report=xml -vvvv

# Validate the schema of the generated statistics file
validate-schema:
    uv run check-jsonschema --schemafile tests/schema_validation/repositories_schema.json tests/schema_validation/repositories.json

# ------------------------------------------------------------------------------
# Cleaning Commands
# ------------------------------------------------------------------------------

# Remove all cloned repositories and generated files
clean:
    just clean-repos
    just clean-generated-files
    find . \( \
      -name '__pycache__' -o \
      -name '.coverage' -o \
      -name '.mypy_cache' -o \
      -name '.pytest_cache' -o \
      -name '.ruff_cache' -o \
      -name '*.pyc' -o \
      -name '*.pyd' -o \
      -name '*.pyo' -o \
      -name 'coverage.xml' -o \
      -name 'db.sqlite3' \
    \) -print | xargs rm -rfv

# Remove all cloned repositories
clean-repos:
    rm -rf validator/cloned_repositories/** || true

# Remove all generated files from running validator
clean-generated-files:
    rm repositories.json || true

# ------------------------------------------------------------------------------
# Docker Commands
# ------------------------------------------------------------------------------

# Build the Docker image
docker-build:
    docker build -t jackplowman/repo_standards_validator:latest .

# Run the validator in a Docker container, used for testing the github action docker image
docker-run:
    docker run \
      --env GITHUB_TOKEN=${GITHUB_TOKEN} \
      --env INPUT_REPOSITORY_OWNER=JackPlowman \
      --volume "$(pwd)/validator:/validator" \
      --rm jackplowman/repo_standards_validator:latest

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formatting
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just ruff-format-fix
    just ruff-lint-fix

# Check for all Ruff issues
ruff-checks:
    just ruff-format-check
    just ruff-lint-check

# Check for Ruff issues
ruff-lint-check:
    uv run ruff check .

# Fix Ruff lint issues
ruff-lint-fix:
    uv run ruff check . --fix

# Check for Ruff format issues
ruff-format-check:
    uv run ruff format --check .

# Fix Ruff format issues
ruff-format-fix:
    uv run ruff format .

# ------------------------------------------------------------------------------
# Ty - Python Type Checking
# ------------------------------------------------------------------------------

# Check for type issues with Ty
ty-check:
    uv run ty check .

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

# Check for unused code
vulture:
    uv run vulture validator

uv-lock-check:
    uv lock --check

# ------------------------------------------------------------------------------
# Prettier
# ------------------------------------------------------------------------------

# Check all files with prettier
prettier-check:
    prettier . --check

# Format all files with prettier
prettier-format:
    prettier . --check --write

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

# Format Justfile
format:
    just --fmt --unstable

# Check Justfile formatting
format-check:
    just --fmt --check --unstable

# ------------------------------------------------------------------------------
# Gitleaks
# ------------------------------------------------------------------------------

# Run gitleaks detection
gitleaks-detect:
    gitleaks detect --source .

# ------------------------------------------------------------------------------
# Lefthook
# ------------------------------------------------------------------------------

# Validate lefthook config
lefthook-validate:
    lefthook validate

# ------------------------------------------------------------------------------
# Zizmor
# ------------------------------------------------------------------------------

# Run zizmor checking
zizmor-check:
    uvx zizmor . --persona=auditor

# ------------------------------------------------------------------------------
# Actionlint
# ------------------------------------------------------------------------------

# Run actionlint checks
actionlint-check:
    actionlint

# ------------------------------------------------------------------------------
# Pinact
# ------------------------------------------------------------------------------

# Run pinact
pinact-run:
    pinact run

# Run pinact checking
pinact-check:
    pinact run --verify --check

# Run pinact update
pinact-update:
    pinact run --update

# ------------------------------------------------------------------------------
# EditorConfig
# ------------------------------------------------------------------------------

# Check files format with EditorConfig
editorconfig-check:
    editorconfig-checker

# ------------------------------------------------------------------------------
# Git Hooks
# ------------------------------------------------------------------------------

# Install pre commit hook to run on all commits
install-git-hooks:
    lefthook install -f
