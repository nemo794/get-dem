#!/bin/bash
# This is intended for running DPS jobs.

# The environment.yaml file sets up a custom conda environment called `dem`.
# For NASA MAAP DPS, use `source activate <custom>`, not `conda activate <custom>`
source activate dem

# [left  bottom  right top]
INPUT_LEFT=$1
INPUT_BOTTOM=$2
INPUT_RIGHT=$3
INPUT_TOP=$4

# Get path to this run.sh script
basedir=$( cd "$(dirname "$0")" ; pwd -P )

# Per DPS convention, the directory to place outputs into MUST be called "output".
# Only items in a directory with that name will persist in my-public-bucket after DPS finishes.
mkdir -p output

# Setup the environment variables. (Req'd for sardem)
export HOME=/home/ops

python ${basedir}/get_dem.py --bbox ${INPUT_LEFT} ${INPUT_BOTTOM} ${INPUT_RIGHT} ${INPUT_TOP} --out_dir output

