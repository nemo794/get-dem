#!/usr/bin/env bash

set -xeou pipefail

basedir=$(dirname "$(dirname "$(readlink -f "$0")")")
conda=${CONDA_EXE:-conda}

PIP_REQUIRE_VENV=0 "${conda}" env update --quiet --prune --solver libmamba \
    --name dem --file "${basedir}"/environment.yml
