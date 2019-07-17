#!/bin/bash -l
source /srv/py3_venv/bin/activate
export PYTHONPATH=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/mpi4py_run/official_run:$PYTHONPATH

python ./example1.py $name_for_run
