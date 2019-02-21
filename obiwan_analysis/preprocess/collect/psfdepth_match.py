'''
some of my ouputs have the same psfdepth as dr3 data, some are the same as dr5 data. I want to find the bricks that matches the dr3 data
'''
import os
import astropy.io.fits as fits
import numpy as np
#data dir for dr3
dr3_tractor_dir = os.environ['dr3_tractor_data']
dr5_tractor_dir = '/global/project/projectdirs/cosmo/data/legacysurvey/dr5/tractor/'
#data for my obiwan output
obiwan_dir = os.environ['production_run_sgc']
def perbrick_match(brickname):
    try:
       dr3_tractor = fits.getdata(os.path.join(dr3_tractor_dir, brickname[:3], 'tractor-'+brickname+'.fits'))
       dr5_tractor = fits.getdata(os.path.join(dr5_tractor_dir, brickname[:3], 'tractor-'+brickname+'.fits'))
    except:
       return None
    obiwan = fits.getdata(os.path.join(os.environ['production_run_sgc'],brickname[:3],brickname,'more_rs0','tractor-'+brickname+'.fits'))
    psfdepthg_dr3 = np.array(list(set(dr3_tractor['DECAM_DEPTH'].transpose()[1])))
    psfdepthg_dr5 = np.array(list(set(dr5_tractor['psfdepth_g'])))
    psfdepthg_obiwan = np.array(list(set(obiwan['psfdepth_g'])))
    in_dr3 = True
    in_dr5 = True
    for p_obiwan in psfdepthg_obiwan:
        dr3_check = np.fabs(psfdepthg_dr3 - p_obiwan).min()
        dr5_check = np.fabs(psfdepthg_dr5 - p_obiwan).min()
        if dr3_check>8:
            in_dr3 = False 
        if dr5_check>8:
            in_dr5 = False
    print('%s in dr3 is %r, in dr5 is %r' %(brickname, in_dr3, in_dr5))
    if in_dr3:
       f = open('dr3_bricks.txt','a')
       f.write(brickname+'\n')
       f.close()
    elif in_dr5:
       f = open('dr5_bricks.txt','a')
       f.write(brickname+'\n')
       f.close()
    else:
       f = open('non_dr_bricks.txt','a')
       f.write(brickname+'\n')
       f.close()
def match():
    fn_PB = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_200per_run/FinishedBricks.txt'
    PB = np.loadtxt(fn_PB, dtype = np.str)
    f = open('dr3_bricks.txt','w')
    f.close()
    f = open('dr5_bricks.txt','w')
    f.close()
    f = open('non_dr_bricks.txt','w')
    f.close()
    for brickname in PB:
        perbrick_match(brickname)

match()
