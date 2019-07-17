#!/bin/bash -l

#SBATCH -p debug
#SBATCH -N 30
#SBATCH -t 00:30:00
#SBATCH --account=desi
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL
module swap python/2.7-anaconda-5.2 python/3.6-anaconda-5.2 
module load python/3.6-anaconda-5.2
source activate myenv 
export PYTHONPATH=.:$PYTHONPATH

#srun -N 10 -n 640 -c 1 python3 example1.py eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk23_elg_ngc_run_obiwan_weight_z_subset eBOSS_ELG_clustering_eboss23_v4.ran_obiwan_weight_subset elg_clustering_chunk23_w_edge_uniform_all

#srun -N 30 -n 1920 -c 1 python3 example1.py  eBOSS_ELG_clustering_NGC_v5.dat_subset eBOSS_ELG_clustering_NGC_v5.ran_subset elg_clustering_ngc_v5

srun -N 30 -n 1920 -c 1 python3 example1.py eBOSS_ELG_clustering_eboss23_v5.dat_obiwan_weight_subset eBOSS_ELG_clustering_eboss23_v5.ran_obiwan_weight_subset elg_ngc_run_conbimed_weight_systot
