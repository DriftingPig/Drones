from Splitfile import *
import os
from file_system import *
import subprocess
name ='elg_clustering_chunk23_w_edge'
Type = 'uniform' 
weight_col = [ 'obiwan_weight','WEIGHT_CP','WEIGHT_NOZ'] #['WEIGHT_SYSTOT', 'WEIGHT_CP', 'WEIGHT_NOZ']
function_name = name

dirs = surveyname(name, Type)
func_name = 'dirs.'+function_name
func = eval(func_name) 
func()
names = survey(dirs)

random_data = names.rawdata_random
dat_data = names.rawdata_data

print(dirs.splitfile_topdir+random_data)
def spltfls():
    if Type == 'obiwan':
        pix_list = splitfile_random(random_data,dirs.splitfile_topdir,use_weight=True, weight_col = weight_col, z_colname='Z')
    else:
        #import pdb
        #pdb.set_trace()
        pix_list = splitfile_random(random_data,dirs.splitfile_topdir,use_weight=True, weight_col = weight_col, z_colname='Z') #, random_z = True, dat_fn = dat_data)
    splitfile_data(dat_data,dirs.splitfile_topdir,pix_list,use_weight=True, weight_col = weight_col, z_colname='Z')

spltfls()

#./NewData_MultiRun.sh 'elg_240_sgc.v2.TSR.SSR.chunk21_subset' 'random-sweep.merged.chunk21_TSR_SSR_subset' 
fn_dat = os.path.basename(dat_data).replace('.fits','_subset')
fn_random = os.path.basename(random_data).replace('.fits','_subset')
print(random_data)
import subprocess
subprocess.call(["mkdir","-p",dirs.splitfile_topdir])
print("./NewData_MultiRun.sh %s %s %s" %(fn_dat,fn_random,name))
#subprocess.call("./NewData_MultiRun.sh", fn_dat, fn_random)
