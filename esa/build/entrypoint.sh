#!/bin/sh

set -ex
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# ESA DPS command-line is --bbox ${BBOX} --compute ${COMPUTE}
# ${BBOX} : bounding box coordinate
# ${COMPUTE} TRUE (case insensitive) to activate heavy load computation

BBOX=$2
COMPUTE=$4

if echo "$COMPUTE" | grep -i true; then
    DO_COMPUTE="--compute"
else
    DO_COMPUTE=""
fi

# Creating output folder
outdir="/projects/data/output"
mkdir -p "${outdir}"

cd /projects

# shellcheck disable=SC2086
python -m scalene --no-browser --json --outfile "${outdir}/profile.json" --- \
    /opt/get-dem/get_dem.py -o /projects/data/output --bbox ${BBOX} ${DO_COMPUTE}

find "${outdir}" -type f
