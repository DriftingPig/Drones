#!/bin/bash -l

#SBATCH -p debug
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH --account=desi
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL

# NERSC / Cray / Cori / Cori KNL things
export KMP_AFFINITY=disabled
export MPICH_GNI_FORK_MODE=FULLCOPY
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
# Protect against astropy configs
export XDG_CONFIG_HOME=/dev/shm

load_desiconda

srun -N 1 -n 1 -c 64 ./vetomask
