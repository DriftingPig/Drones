'''
merge all sim randoms per brick to one fits file
'''
import astropy.io.fits as fits
import numpy as np
import os
from glob import glob
from numpy.random import normal
topdir_randoms = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat_2/'
fn_PB=os.path.join(os.environ['DRONES_DIR'],'obiwan_analysis/brickstat/FinishedBricks.txt')
PB = np.loadtxt(fn_PB,dtype=np.str)

def fn_finder(brickname):
    return topdir_randoms+'brick_'+brickname+'.fits'

def BrickMerge():
    dat = np.array(fits.open(fn_finder(PB[0]))[1].data[:200])
    for i in range(1,len(PB)):
        print(PB[i])
        dat_i = np.array(fits.open(fn_finder(PB[i]))[1].data[:200])
        dat = np.hstack((dat,dat_i))
    cols = fits.ColDefs(dat)
    HDU = fits.BinTableHDU.from_columns(cols)
    HDU.writeto(os.path.join(os.environ['obiwan_out'],'subset/sim_200per_0125.fits'), overwrite=True)


BrickMerge() 
