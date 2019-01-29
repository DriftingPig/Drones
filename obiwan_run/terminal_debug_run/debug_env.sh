#!/bin/bash -l

export name_for_run=elg_eight_bricks
export randoms_db=None
export dataset=dr3
export rowstart=0
export do_skipids=no
export do_more=no
export minid=1
export object=elg
export nobj=200

export usecores=1
export threads=1
export CSCRATCH=/global/cscratch1/sd/huikong
export CSCRATCH_OBIWAN=$CSCRATCH/obiwan_Aug/repos_for_docker
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH

export obiwan_data=$CSCRATCH_OBIWAN/obiwan_data
export obiwan_code=$CSCRATCH_OBIWAN/obiwan_code
export obiwan_out=$CSCRATCH_OBIWAN/obiwan_out

export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH

shifter --image=driftingpig/obiwan_composit:v3 /bin/bash

