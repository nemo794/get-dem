#!/bin/bash

basedir=$( cd "$(dirname "$0")" ; pwd -P )
REPO_ROOT_PATH=$(dirname ${basedir})

conda config --set solver libmamba

conda env create -f ${REPO_ROOT_PATH}/environment.yaml

