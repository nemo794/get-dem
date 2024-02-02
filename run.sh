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
COMPUTE=$5

echo $INPUT_LEFT
echo $INPUT_BOTTOM
echo $INPUT_RIGHT
echo $INPUT_TOP
echo $COMPUTE


# Get path to this run.sh script
basedir=$( cd "$(dirname "$0")" ; pwd -P )

# Per NASA MAAP DPS convention, all outputs MUST be placed
# by the algorithm into a directory called "output".
# Once the DPS job finishes, MAAP will copy everything from "output"
# to a directory in my-public-bucket. Everything else on the instance
# will be destroyed.
mkdir -p output

# Setup the environment variables. (Req'd for sardem)
export HOME=/home/ops

python ${basedir}/get_dem.py --bbox ${INPUT_LEFT} ${INPUT_BOTTOM} ${INPUT_RIGHT} ${INPUT_TOP} ${COMPUTE} --out_dir output

