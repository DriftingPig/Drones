from file_system import *
#fn_PB='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_200per_run/FinishedBricks.txt'
#fn_PB='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/collect/cutted_bricks.txt'
#name = 'obiwan_run_set2_step1'
fn_PB = 
name = 'obiwan_run_set2_step2_chunk22'

func_name = name
dirs = surveyname(name,'uniform')
func = eval('dirs.'+func_name)
func()
name = survey(dirs)
data_file = name.rawdata_data
print(data_file)
output_dir = dirs.raw_topdir
import os
import astropy.io.fits as fits
import numpy as np
bn = os.path.basename(data_file)
output_fn = output_dir+bn[:-5]+'_cutted.fits'
dat_PB = np.loadtxt(fn_PB,dtype=np.str)

dat = fits.open(data_file)[1].data[::]
print(len(dat))
dat = fits.BinTableHDU.from_columns(fits.ColDefs(np.array(dat))).data
#print len(dat)
flag = np.zeros(len(dat),dtype = bool)
for i in range(len(dat)):
    if dat['brickname'][i] in dat_PB:
          flag[i]=True
dat_sel = np.array(dat[flag])
fits.BinTableHDU.from_columns(fits.ColDefs(dat_sel)).writeto(output_fn,overwrite=True)
print(output_fn)
