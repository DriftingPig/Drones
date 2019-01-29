#preprocess the data, and make it fit for testing correlation functions
'''
1. cut data to the same foot print
2. mask everything (data, obiwan, sim), separate them as chunk21, chunk22
3. write the processed files to $obiwan_out/subset

Output: all three files with 'processed' appending at the end of the filename

Version 1:
01/25/2019
'''
import numpy as np
import astropy.io.fits as fits
import os
data_fn = 'ELG.v5_11_0.rrv2.all.fits'
obiwan_fn = 'obiwan_200per_1125.fits'
sim_fn = 'sim_200per_1125.fits'
PB_fn = os.path.join(os.environ['DRONES_DIR'],'obiwan_analysis/brickstat/FinishedBricks.txt')
bricklist = np.loadtxt(PB_fn,dtype=np.str).transpose()

topdir = os.path.join(os.environ['obiwan_out'],'subset')
data = fits.open(os.path.join(topdir,data_fn))[1].data
obiwan = fits.open(os.path.join(topdir,obiwan_fn))[1].data
sim = fits.open(os.path.join(topdir,sim_fn))[1].data

def data_footprint_cut(bricklist = bricklist, data = data):
    #cut data to only the bricks provided in the processed brick list
    flag = np.zeros(len(dat),dtype = bool)
    for i in range(len(dat)):
       if dat['brickname'][i] in bricklist:
          flag[i]=True
    dat_sel = np.array(dat[flag])
    return fits.BinTableHDU.from_columns(fits.ColDefs(dat_sel)).data
