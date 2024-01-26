#!/bin/bash

basedir=$( cd "$(dirname "$0")" ; pwd -P )
conda config --set solver libmamba

conda env create -f ${basedir}/environment.yaml

