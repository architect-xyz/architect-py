#!/bin/bash -e
#
# This script checks that the version in pyproject.toml matches the __version__ in __init__.py

PYPROJECT_VERSION=$(sed -n 's/^version = "\([^"]*\)".*/\1/p' ./pyproject.toml)
INIT_VERSION=$(sed -n 's/^__version__ = "\([^"]*\)".*/\1/p' ./architect_py/__init__.py)

if [ -z "$PYPROJECT_VERSION" ]; then
    echo "Error: could not find version in pyproject.toml"
    exit 1
fi

if [ -z "$INIT_VERSION" ]; then
    echo "Error: could not find version in __init__.py"
    exit 1
fi


if [ "$PYPROJECT_VERSION" != "$INIT_VERSION" ]; then
    echo "Error: version mismatch"
    echo ""
    echo "pyproject.toml = $PYPROJECT_VERSION"
    echo "__init__.py = $INIT_VERSION"
    exit 1
fi

echo -e "\033[32mOK\033[0m $PYPROJECT_VERSION" 
