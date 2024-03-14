#!/bin/sh

set -x
export LC_ALL=C.UTF-8
export LANG=C.UTF-8


# ESA DPS command-line is --bbox ${BBOX} --compute ${COMPUTE} 
# ${BBOX} : bounding box coordinate
# ${COMPUTE} TRUE / FALSE to activate heavy load computation

BBOX=$2
COMPUTE=$4

if [ $COMPUTE = "TRUE" ]; then
    DO_COMPUTE="--compute"
else
    DO_COMPUTE=""
fi


# Creating output folder
mkdir -p /projects/data/output

cd /projects

python3 /opt/get-dem/get_dem.py -o /projects/data/output --bbox ${BBOX} ${DO_COMPUTE} 

find /projects/data/output -type f