#!/bin/bash -l

#SBATCH -p debug
#SBATCH -N 25
#SBATCH -t 00:30:00
#SBATCH --account=desi
#SBATCH --image=driftingpig/obiwan_composit:v3
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL

export name_for_run=chunk21_new_calib
export tot_bricks=10219
export random_name=sgc_brick_dat_2
export randoms_db=None
export dataset=dr3
export rowstart=0 
export do_skipids=no  
export do_more=no 
export minid=1  
export object=elg   
export nobj=5

export usecores=64
export threads=64
export CSCRATCH_OBIWAN=$CSCRATCH/obiwan_Aug/repos_for_docker  
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH 

export obiwan_data=$CSCRATCH_OBIWAN/obiwan_data
export obiwan_code=$CSCRATCH_OBIWAN/obiwan_code
export obiwan_out=$CSCRATCH_OBIWAN/obiwan_out  

# NERSC / Cray / Cori / Cori KNL things 
export KMP_AFFINITY=disabled  
export MPICH_GNI_FORK_MODE=FULLCOPY 
export MKL_NUM_THREADS=1 
export OMP_NUM_THREADS=1   
# Protect against astropy configs 
export XDG_CONFIG_HOME=/dev/shm   
srun -n $SLURM_JOB_NUM_NODES mkdir -p $XDG_CONFIG_HOME/astropy

srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 0 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 1 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 2 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 3 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 4 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 5 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 6 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 7 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 8 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 9 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 10 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 11 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 12 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 13 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 14 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 15 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 16 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 17 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 18 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 19 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 20 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 21 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 22 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 23 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 24 &
srun -N 1 -n 1 -c $usecores shifter ./real_brick_scheduler.sh 25 &
wait



