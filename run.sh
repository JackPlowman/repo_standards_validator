#!/bin/sh
set -e +x

if [ "$CI" = "true" ]; then
  # if running in GitHub Actions, change to the root of the repository
  cd ..
  cd ..
fi

# Run the analyser
python -m validator

if [ "$CI" = "true" ]; then
  # if running in GitHub Actions, copy the output to the output directory
  cp statistics/repositories.json github/workspace/repositories.json
  echo "Copied statistics to github/workspace"
fi
