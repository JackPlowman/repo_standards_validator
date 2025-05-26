#!/bin/bash
set -e +x

# check file exists
test -f repositories.json

# check file is not empty
test -s repositories.json
