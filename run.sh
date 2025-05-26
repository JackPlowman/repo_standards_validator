#!/bin/sh
set -e +x

if [ "$CI" = "true" ]; then
  # if running in GitHub Actions, change to the root of the repository
  cd ..
  cd ..
fi

# Run validator
python -m validator

if [ "$CI" = "true" ]; then
  # if running in GitHub Actions, copy the output to the output directory
  cp repositories.json github/workspace/repositories.json
  echo "Copied repositories.json to github/workspace"
fi
