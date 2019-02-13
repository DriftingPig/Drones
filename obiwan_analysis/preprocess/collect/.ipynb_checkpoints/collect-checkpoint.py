'''
collect all the tractor outputs in one file, specify colum names for sim files and tractor fils to be collected, specify angular distance to be considered as matched

version 1:
01/24/2019

version 2:
02/11/2019
'''

'''
for eBOSS sgc runs, the mean angular diameter distance is 0.5" due to some unknown reasons, so we choose the matched scale as 1.5" to fulfill a 1" match 
'''

import os
import glob
import numpy as n
import numpy as np
from astropy.io import fits
from math import *
from astropy.table import Column, Table
from astropy.coordinates import SkyCoord
from astropy import units as u
import subprocess

#subprocess.run(['source','../DRONES_ENV.sh'])
assert(os.environ['DRONES_ACTIVATION']=='True')

#initialize all the directories
tractor_dir = os.environ['production_run_sgc']
dr3_tractor_dir = os.environ['dr3_tractor_data']
sim_dir = os.path.join(os.environ['obiwan_out'],'eboss_elg/sgc_brick_dat_2')
PB_fn = os.path.join(os.environ['DRONES_DIR'],'obiwan_analysis/brickstat/FinishedBricks.txt')
bricklist = np.loadtxt(PB_fn,dtype=np.str).transpose()

def select_ELG( path_2_tractor_file , region = 'sgc'):
    """
    Given the path to a tractor catalog, it returns two sub catalogs with the eBOSS ELG selections applied (NGC and SGC).
    """

    # opens the tractor file
    hdu=fits.open(path_2_tractor_file)
    dat=hdu[1].data
    hdu.close()
    # the color color selection
    g     = 22.5 - 2.5 * n.log10(dat['flux_g'] / dat['mw_transmission_g'])
    r_mag = 22.5 - 2.5 * n.log10(dat['flux_r'] / dat['mw_transmission_r'])
    z_mag = 22.5 - 2.5 * n.log10(dat['flux_z'] / dat['mw_transmission_z'])
    gr = g - r_mag
    rz = r_mag - z_mag
    color_sgc = (g>21.825)&(g<22.825)&(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.218*gr+0.571<rz)&(rz<-0.555*gr+1.901)
    color_ngc = (g>21.825)&(g<22.9)  &(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.637*gr+0.399<rz)&(rz<-0.555*gr+1.901) 
    # the junk rejection criterion
    noJunk = (dat['brick_primary']) & (dat['anymask_g']==0) & (dat['anymask_r']==0) & (dat['anymask_z']==0) #& (dat['TYCHO2INBLOB']==False)
    # the low depth region rejection
    value_g=dat['psfdepth_g']
    value_r=dat['psfdepth_r']
    value_z=dat['psfdepth_z']
    gL = 62.79716079 
    rL = 30.05661087
    zL_ngc = 11.0
    zL_sgc = 12.75  
    depth_selection_ngc = (value_g > gL) & (value_r > rL) & (value_z > zL_ngc)
    depth_selection_sgc = (value_g > gL) & (value_r > rL) & (value_z > zL_sgc)
    # final selection boolean array :
    selection_sgc =(noJunk)&(color_sgc)&(depth_selection_sgc)
    selection_ngc =(noJunk)&(color_ngc)&(depth_selection_ngc)
    # returns the catalogs of ELGs
    if region == 'sgc':
        if len(selection_sgc.nonzero()[0])>0:
            flag = True
            return flag, dat[selection_sgc]
        else:
            flag = False
            return flag, dat[selection_sgc]
    if region == 'ngc':
            if len(selection_ngc.nonzero()[0])>0 :
                flag = True
                return flag, dat[selection_ngc]
            else:
                flag = False
                return flag, dat[selection_ngc] 

def select_ELG_sim(sim_dat, region = 'sgc'):
    g = sim_dat['g']
    r_mag = sim_dat['r']
    z_mag = sim_dat['z']
    gr = g - r_mag
    rz = r_mag - z_mag
    color_sgc = (g>21.825)&(g<22.825)&(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.218*gr+0.571<rz)&(rz<-0.555*gr+1.901)
    color_ngc = (g>21.825)&(g<22.9)  &(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.637*gr+0.399<rz)&(rz<-0.555*gr+1.901)
    if region == 'sgc':
         return color_sgc
    else:
         return color_ngc
          
def ELG_match(index, angle = 1.5/3600., tractor_dir = tractor_dir, sim_dir = sim_dir, bricklist=bricklist, startid = 0, nobj = 200, region = 'sgc'):
    brickname = bricklist[index]
    tractor_fn = os.path.join(tractor_dir, brickname[:3], brickname, 'more_rs0', 'tractor-'+brickname+'.fits')
    assert(os.path.isfile(tractor_fn))
    sim_fn = os.path.join(sim_dir, 'brick_'+brickname+'.fits')
    assert(os.path.isfile(sim_fn))
    flag_tc, tractor_dat = select_ELG(tractor_fn, region = region)
    if flag_tc is False:
        return None
    sim_hdu = fits.open(sim_fn)
    sim_dat = sim_hdu[1].data[startid:startid+nobj]
    sim_hdu.close()
    c1 = SkyCoord(ra=tractor_dat['ra']*u.degree, dec=tractor_dat['dec']*u.degree)
    c2 = SkyCoord(ra=sim_dat['ra']*u.degree, dec=sim_dat['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    distance = d2d.value[w]
    print(len(tractor_dat[idx1]), len(sim_dat[idx2]))
    
    mtc = tractor_dat[idx1]
    msim = sim_dat[idx2]
    brickname_array = np.array([brickname]*len(mtc),dtype = np.str)
    angdis = d2d.value[idx1]
    tab = Table([mtc['ra'],mtc['dec'],mtc['flux_z'],mtc['mw_transmission_z'],msim['z'],mtc['flux_g'],mtc['mw_transmission_g'],msim['g'],mtc['flux_r'],mtc['mw_transmission_r'],msim['r'],msim['nn_redshift'],brickname_array,angdis,msim['n'],mtc['fracdev'],mtc['shapeexp_r'],mtc['shapedev_r'],msim['rhalf']],names=('ra','dec','flux_z','mw_transmission_z','z','flux_g','mw_transmission_g','g','flux_r','mw_transmission_r','r','nn_redshift','brickname','angdis','n','fracdev','shapeexp_r','shapedev_r','rhalf'))
    return tab
 
def sim_pre_match(sim_dat, obiwan_dat, angle = 1.5/3600.):
    c1 = SkyCoord(ra = obiwan_dat['ra']*u.degree, dec = obiwan_dat['dec']*u.degree)
    c2 = SkyCoord(ra = sim_dat['ra']*u.degree, dec = sim_dat['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    idx2 = idx[idx>-1]
    return sim_dat[idx2]

def sim_match(index, angle = 1.5/3600., tractor_dir = tractor_dir, sim_dir = sim_dir, bricklist=bricklist, startid = 0, nobj = 200, region = 'sgc'):
    #get info for the number of tc been selected as elg/non-elg wrong or right
    brickname = bricklist[index]
    tractor_fn = os.path.join(tractor_dir, brickname[:3], brickname, 'more_rs0', 'tractor-'+brickname+'.fits')
    assert(os.path.isfile(tractor_fn))
    sim_fn = os.path.join(sim_dir, 'brick_'+brickname+'.fits')
    assert(os.path.isfile(sim_fn))
    flag_tc, tractor_dat = select_ELG(tractor_fn, region = region)
    sim_hdu = fits.open(sim_fn)
    sim_dat = sim_hdu[1].data[startid:startid+nobj]
    sim_hdu.close()
    obiwan_dat = fits.getdata(tractor_fn)
    sim_dat = sim_pre_match(sim_dat,obiwan_dat)
    c1 = SkyCoord(ra=tractor_dat['ra']*u.degree, dec=tractor_dat['dec']*u.degree)
    c2 = SkyCoord(ra=sim_dat['ra']*u.degree, dec=sim_dat['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    sim_in = np.zeros(len(sim_dat),dtype = bool)
    sim_in[idx2] = True
    sim_elg_sel = select_ELG_sim(sim_dat)
    sim_true = np.zeros(len(sim_dat),dtype = bool)
    sim_true[sim_elg_sel] = True
    tab = Table([sim_dat['ra'],sim_dat['dec'],sim_dat['nn_redshift'],sim_in,sim_true],names=('ra','dec','nn_redshift','sim_in','sim_true'))
    return tab 


def elg_dr3_match_perbrick(index,angle = 0.1/3600):
    #match elg data to dr3 cat to get info for rhalf
    elg_fn = os.path.join(os.environ['obiwan_out'],'subset/eBOSS_ELG_full_ALL_v4.dat.fits')
    elg_dat = fits.getdata(elg_fn)
    brickname = bricklist[index]
    dr3_tractor_fn = os.path.join(os.environ['dr3_tractor_data'], brickname[:3], 'tractor-'+brickname+'.fits') 
    try:
        dr3_tractor_dat = fits.getdata(dr3_tractor_fn)
    except:
        return None
    c1 = SkyCoord(ra=elg_dat['ra']*u.degree, dec=elg_dat['dec']*u.degree)
    c2 = SkyCoord(ra=dr3_tractor_dat['RA']*u.degree, dec=dr3_tractor_dat['DEC']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    distance = d2d.value[w]
    print(len(elg_dat[idx1]), len(dr3_tractor_dat[idx2]))
    elg = elg_dat[idx1]
    dr3 = dr3_tractor_dat[idx2]
    
    from astropy.table import hstack
    tab2 = Table([dr3['fracDev'],dr3['shapeExp_r'],dr3['shapeDev_r'],dr3['shapeExp_e1'],dr3['shapeExp_e2'],dr3['shapeDev_e1'],dr3['shapeDev_e2'],distance],names=('fracDev','shapeExp_r','shapeDev_r','shapeExp_e1','shapeExp_e2','shapeDev_e1','shapeDev_e2',distance))
    elg_tab = Table(elg)
    return hstack(elg_tab,tab2)