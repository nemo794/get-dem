#!/usr/bin/env bash

set -xeou pipefail

basedir=$(dirname "$(dirname "$(readlink -f "$0")")")
conda=${CONDA_EXE:-conda}

# Install main dependencies
"${basedir}/nasa/build-dps.sh"

# Install development dependencies
PIP_REQUIRE_VENV=0 "${conda}" env update --quiet --solver libmamba \
    --name dem --file "${basedir}/nasa/environment-dev.yml"

# Install the kernel for Jupyter
"${conda}" run --name dem \
    python -Xfrozen_modules=off -m ipykernel install \
    --user --name dem --display-name "Get DEM (Python)"
