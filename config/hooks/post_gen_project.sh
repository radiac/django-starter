#!/bin/bash
set -e

# Check if the current directory is a git repo
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    UPGRADE=1
    echo "Existing project found, upgrading in place"
else
    UPGRADE=0
    echo "No existing project found, creating new"
fi

# If UPGRADE is 1, check it looks like we're upgrading one of our projects
if [ "$UPGRADE" -eq 1 ]; then
    if ! git log --grep='^radiac/django-sta{##}rter' --oneline | grep -q .; then
        echo "Error: No commits found for 'radiac/django-sta{##}rter'."
        exit 1
    fi
fi

# Don't touch the venv if upgrading
if [ "$UPGRADE" -eq 0 ]; then
    python -m venv .venv
    source .venv/bin/activate
    pip install uv pre-commit

    uv pip compile requirements.in -o requirements.txt
    uv pip sync requirements.txt

    cp compose.dev.yaml compose.yaml
fi

# Assume a git repo if upgrading
if [ "$UPGRADE" -eq 0 ]; then
    git init
fi

# Upgrades should commit
git add .
git commit -m "radiac/django-sta{##}rter v{{ cookiecutter._version }}"

# Assume pre-commit already installed if upgrading
if [ "$UPGRADE" -eq 0 ]; then
    pre-commit install
fi
