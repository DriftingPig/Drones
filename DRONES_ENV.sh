#!/bin/bash -l

#source this file before performing any obiwan production runs or obiwan analysis

#for determining whether this file is sourced
export DRONES_ACTIVATION=True

#DRONES current directory
export DRONES_DIR=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones

#some excecutable python packages: master-slave code
export PYTHONPATH=$DRONES_DIR/py:$PYTHONPATH

#general output directory for obiwan production run
export obiwan_out=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/

#obiwan production run output directory, it comes with a production run name
export production_run_sgc=$obiwan_out/elg_200per_run/

export production_run_sgc_sim=$obiwan_out/elg_200per_run/obiwan/
#tractor data for dr3
export dr3_tractor_data=/global/project/projectdirs/cosmo/data/legacysurvey/dr3/tractor

#NGC run by kaylan
export NGC_tractor=/global/cscratch1/sd/huikong/obiwan_Aug/HPSS/tractor
export NGC_sim=/global/cscratch1/sd/huikong/obiwan_Aug/HPSS/obiwan

export elg_ngc_run=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_ngc_run/

export elg_like_run=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_like_run/

export chunk21_10deg2_test=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/chunk21_10deg2_test/
