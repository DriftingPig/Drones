'''
some of my ouputs have the same psfdepth as dr3 data, some are the same as dr5 data. I want to find the bricks that matches the dr3 data
'''
import os
import astropy.io.fits as fits
import numpy as np
#data dir for real elgs
topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
elg_chunk21_fn = topdir + 'eBOSS_ELG_full_ALL_v4.dat_cutted_really_masked_chunk21.fits'
elg_chunk22_fn = topdir + 'eBOSS_ELG_full_ALL_v4.dat_really_masked_cutted.fits'
#data for my obiwan output
obiwan_dir = os.environ['production_run_sgc']
f = open('elg_obiwan_compare_bricks.txt','w')
f.close()
f = open('elg_obiwan_compare_bricks.txt','a')
def perbrick_match(brickname):
    elg_chunk21 = fits.getdata(elg_chunk21_fn)
    elg_chunk22 = fits.getdata(elg_chunk22_fn)
    if brickname in elg_chunk21['brickname']:
       elg = elg_chunk21
    elif brickname in elg_chunk22['brickname']:
       elg = elg_chunk22
    else:
       print('NOTICE!!! no such brick %s' %brickname)
       return None
    elg_in_brick = elg[elg['brickname']==brickname]
    obiwan = fits.getdata(os.path.join(os.environ['production_run_sgc'],brickname[:3],brickname,'more_rs0','tractor-'+brickname+'.fits'))
    psfdepthg_elg = np.array(list(set(elg_in_brick['psfdepth_g'])))
    psfdepthg_obiwan = np.array(list(set(obiwan['psfdepth_g'])))
    count = 0
    tot = 0
    for p_elg in psfdepthg_elg:
        elg_check = np.fabs(psfdepthg_obiwan - p_elg).min()
        tot+=elg_check
        count+=1
    mean = float(tot)/float(count)
    print('%s %.3f' %(brickname, mean))
    f.write('%s %.3f\n' %(brickname, mean))
    return None

def match():
    fn_PB = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_200per_run/FinishedBricks.txt'
    PB = np.loadtxt(fn_PB, dtype = np.str)
    from multiprocessing import Pool
    p = Pool(32)
    p.map(perbrick_match,PB)
    f.close()
match()
