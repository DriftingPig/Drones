import subprocess
#subprocess.call(['./NewData_CorrFun', '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23_w_edge_debug/splitdata/uniform/eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk23_elg_ngc_run_obiwan_weight_z_subset0.fits', '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23_w_edge_debug/splitdata/uniform/eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk23_elg_ngc_run_obiwan_weight_z_subset1.fits', "5", "0", "1", '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23_w_edge_debug/BinHist/uniform/D0D1.dat', '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23_w_edge_debug/BinHist/uniform/TotalPoints.txt'])
#print('test')
topdir1 = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23_w_edge_weight_systot/BinHist/uniform/'
topdir2 = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23_w_edge_debug/BinHist/uniform/'
import pdb
#pdb.set_trace()

for i in range(0,20):
   for j in range(i,20):
        subprocess.call(["diff",topdir1+'D'+str(i)+'D'+str(j)+'.dat',topdir2+'D'+str(i)+'D'+str(j)+'.dat'])
        #print(["diff",topdir1+'D'+str(i)+'D'+str(j)+'.dat',topdir2+'D'+str(i)+'D'+str(j)+'.dat'])
        #raise


for i in range(0,20):
   for j in range(i,20):
        subprocess.call(["diff",topdir1+'R'+str(i)+'R'+str(j)+'.dat',topdir2+'R'+str(i)+'R'+str(j)+'.dat'])

for i in range(0,20):
   for j in range(0,20):
        subprocess.call(["diff",topdir1+'D'+str(i)+'R'+str(j)+'.dat',topdir2+'D'+str(i)+'R'+str(j)+'.dat'])

