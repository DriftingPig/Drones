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
from astropy.table import hstack

#subprocess.run(['source','../DRONES_ENV.sh'])
assert(os.environ['DRONES_ACTIVATION']=='True')

#initialize all the directories
#tractor_dir = os.environ['production_run_sgc']
#dr3_tractor_dir = os.environ['dr3_tractor_data']
#sim_dir = os.path.join(os.environ['obiwan_out'],'eboss_elg/sgc_brick_dat_2')
#PB_fn = os.path.join(os.environ['DRONES_DIR'],'obiwan_analysis/brickstat/FinishedBricks.txt')
#bricklist = np.loadtxt(PB_fn,dtype=np.str).transpose()

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


def select_ELG_like(path_2_tractor_file , region = 'sgc'):
    """
    Given the path to a tractor catalog, it returns two sub catalogs with the eBOSS ELG selections applied (NGC and SGC).
    update some selection criteria for contaimiation in ELGs
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
    color_sgc = (g>21.0)&(g<23.2)&(-0.068*rz+0.457<gr+0.3)&(0.112*rz+0.773>gr-0.2) &(0.218*gr+0.571<rz+0.3)&(rz-0.3<-0.555*gr+1.901)
    color_ngc = (g>21.0)&(g<23.2)  &(-0.068*rz+0.457<gr+0.3)&(gr-0.2< 0.112*rz+0.773) &(0.637*gr+0.399<rz+0.3)&(rz-0.3<-0.555*gr+1.901)
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
          
def ELG_match(index, angle = 1.5/3600., tractor_dir = None, sim_dir = None, bricklist=None, startid = 0, nobj = 200, region = None):
    assert(tractor_dir is not None);assert(sim_dir is not None);assert(bricklist is not None);assert(region is not None)
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

def sim_match(index, angle = 1.5/3600., tractor_dir = None, sim_dir = None, bricklist=None, startid = 0, nobj = 200, region = None):
    assert(tractor_dir is not None);assert(sim_dir is not None);assert(bricklist is not None);assert(region is not None)
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

def SGC_sim(brickname):
    fn_sim = os.path.join(os.environ['production_run_sgc_sim'],brickname[:3],brickname,'more_rs0','simcat-elg-%s.fits' %brickname)
    sim = fits.getdata(fn_sim)[:200]
    return sim

def sim_PB_cut():
    fn_PB = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/collect/cutted_bricks.txt'
    dat_PB = np.loadtxt(fn_PB,dtype=np.str)
    sim=None
    for brickname in dat_PB:
      print(brickname)
      sim_i = SGC_sim(brickname)
      if sim is None:
         sim = sim_i
      else:
         sim=np.hstack((sim,sim_i)) 
    topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
    fits.BinTableHDU.from_columns(fits.ColDefs(sim)).writeto(topdir+'sim_w_psfdepthcut.fits')

def NGC_sim(brickname):
    fn_sim = os.path.join(os.environ['NGC_sim'],brickname[:3],brickname,'rs0','simcat-elg-%s.fits' %brickname)
    sim = Table.read(fn_sim)
    print(brickname,len(fn_sim)) 
    return sim
def NGC_sim_printer():
    #print HGC brickname #of sims to screen (check #of sims per brick)
    import glob
    from astropy.table import vstack
    paths = glob.glob(os.path.join(os.environ['NGC_tractor'],'*','*'))
    final_tab = None
    for path in paths:
        brickname = os.path.basename(path)
        NGC_sim(brickname)

def NGC_match_perbrick(brickname, angle = 1.5/3600):
    #collecting kaylan's ngc run
    fn_tractor = os.path.join(os.environ['NGC_tractor'],brickname[:3],brickname,'rs0','tractor-%s.fits' %brickname)
    fn_sim = os.path.join(os.environ['NGC_sim'],brickname[:3],brickname,'rs0','simcat-elg-%s.fits' %brickname)
    flag, tractor = select_ELG(fn_tractor, region = 'ngc')
    if flag == False:
        return None
    sim = fits.getdata(fn_sim)
    c1 = SkyCoord(ra=tractor['ra']*u.degree, dec=tractor['dec']*u.degree)
    c2 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    distance = d2d.value[w]
    tc = tractor[idx1]
    sm = sim[idx2]
    tab = Table([tc['ra'],tc['dec'],tc['flux_g'],tc['flux_r'],tc['flux_z'],tc['mw_transmission_g'],tc['mw_transmission_r'],tc['mw_transmission_z'],tc['fracdev'],tc['shapeexp_r'],tc['shapedev_r'],tc['shapeexp_e1'],tc['shapeexp_e2'],tc['shapedev_e1'],tc['shapedev_e2'],sm['id'],sm['gflux'],sm['rflux'],sm['zflux'],sm['mw_transmission_g'],sm['mw_transmission_r'],sm['mw_transmission_z'],sm['rhalf'],sm['n'],sm['e1'],sm['e2']],names=('ra','dec','flux_g','flux_r','flux_z','mw_transmission_g','mw_transmission_r','mw_transmission_z','fracdev','shapeexp_r','shapedev_r','shapeexp_e1','shapeexp_e2','shapedev_e1','shapedev_e2','sim_id','sim_gflux','sim_rflux','sim_zflux','sim_mw_transmission_g','sim_mw_transmission_r','sim_mw_transmission_z','sim_rhalf','sim_n','sim_e1','sim_e2'))
    return tab

def my_NGC_run_perbrick(brickname, angle = 1.5/3600):
    #running my code on ngc bricks, about ~550 finished bricks currently
    fn_tractor = os.path.join(os.environ['my_ngc_run'],'tractor',brickname[:3],brickname,'rs0','tractor-%s.fits' %brickname)
    fn_sim = os.path.join(os.environ['my_ngc_run'],'sim',brickname[:3],brickname,'rs0','simcat-elg-%s.fits' %brickname)
    flag, tractor = select_ELG(fn_tractor, region = 'ngc')
    if flag == False:
        return None,None
    sim = fits.getdata(fn_sim)
    c1 = SkyCoord(ra=tractor['ra']*u.degree, dec=tractor['dec']*u.degree)
    c2 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    distance = d2d.value[w]
    tc = tractor[idx1]
    sm = sim[idx2]
    tab = Table([tc['ra'],tc['dec'],tc['flux_g'],tc['flux_r'],tc['flux_z'],tc['mw_transmission_g'],tc['mw_transmission_r'],tc['mw_transmission_z'],tc['fracdev'],tc['shapeexp_r'],tc['shapedev_r'],tc['shapeexp_e1'],tc['shapeexp_e2'],tc['shapedev_e1'],tc['shapedev_e2'],sm['id'],sm['gflux'],sm['rflux'],sm['zflux'],sm['mw_transmission_g'],sm['mw_transmission_r'],sm['mw_transmission_z'],sm['rhalf'],sm['n'],sm['e1'],sm['e2'],tc['brickname']],names=('ra','dec','flux_g','flux_r','flux_z','mw_transmission_g','mw_transmission_r','mw_transmission_z','fracdev','shapeexp_r','shapedev_r','shapeexp_e1','shapeexp_e2','shapedev_e1','shapedev_e2','sim_id','sim_gflux','sim_rflux','sim_zflux','sim_mw_transmission_g','sim_mw_transmission_r','sim_mw_transmission_z','sim_rhalf','sim_n','sim_e1','sim_e2','brickname'))
    return tab,Table(sim)


def production_run_general_perbrick(brickname, env_dir, rs_type, region ,angle = 1.5/3600):
    #collection of a production run, returns a table of ELGs, a table of sim
    #TODO: something 'might be' useful: sim_ra.sim_dec,sim_z
    fn_tractor = os.path.join(os.environ[env_dir],'tractor',brickname[:3],brickname,rs_type,'tractor-%s.fits' %brickname)
    fn_sim = os.path.join(os.environ[env_dir],'obiwan',brickname[:3],brickname,rs_type,'simcat-elg-%s.fits' %brickname)
    flag, tractor = select_ELG(fn_tractor, region = region)
    if flag == False:
        return None,None
    sim = fits.getdata(fn_sim)
    c1 = SkyCoord(ra=tractor['ra']*u.degree, dec=tractor['dec']*u.degree)
    c2 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    distance = d2d.value[w]
    tc = tractor[idx1]
    sm = sim[idx2]
    tab = Table([tc['ra'],tc['dec'],tc['flux_g'],tc['flux_r'],tc['flux_z'],tc['mw_transmission_g'],tc['mw_transmission_r'],tc['mw_transmission_z'],tc['fracdev'],tc['shapeexp_r'],tc['shapedev_r'],tc['shapeexp_e1'],tc['shapeexp_e2'],tc['shapedev_e1'],tc['shapedev_e2'],sm['id'],sm['gflux'],sm['rflux'],sm['zflux'],sm['mw_transmission_g'],sm['mw_transmission_r'],sm['mw_transmission_z'],sm['rhalf'],sm['n'],sm['e1'],sm['e2'],tc['brickname'],tc['psfdepth_g'],tc['psfdepth_r'],tc['psfdepth_z']],names=('ra','dec','flux_g','flux_r','flux_z','mw_transmission_g','mw_transmission_r','mw_transmission_z','fracdev','shapeexp_r','shapedev_r','shapeexp_e1','shapeexp_e2','shapedev_e1','shapedev_e2','sim_id','sim_gflux','sim_rflux','sim_zflux','sim_mw_transmission_g','sim_mw_transmission_r','sim_mw_transmission_z','sim_rhalf','sim_n','sim_e1','sim_e2','brickname','psfdepth_g','psfdepth_r','psfdepth_z'))
    return tab,Table(sim)


def production_run_general_perbrick_official(brickname, env_dir, rs_type, region, name_for_randoms = None,\
                                             startid = None, nobj = None, sim_topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/',angle = 1.5/3600):
    
    assert(name_for_randoms is not None);assert(startid is not None);assert(nobj is not None)
    print(os.environ[env_dir],brickname,rs_type)
    fn_tractor = os.path.join(os.environ[env_dir],'tractor',brickname[:3],brickname,rs_type,'tractor-%s.fits' %brickname)
    fn_sim = os.path.join(os.environ[env_dir],'obiwan',brickname[:3],brickname,rs_type,'simcat-elg-%s.fits' %brickname)
    fn_original_sim = sim_topdir+name_for_randoms+'/brick_'+brickname+'.fits'
    
    flag, tractor = select_ELG(fn_tractor, region = region)
    
    if flag == False:
        return None,None
    sim = fits.getdata(fn_sim)
    
    original_sim = fits.getdata(fn_original_sim)[startid:startid+nobj] 
    
    c1 = SkyCoord(ra=tractor['ra']*u.degree, dec=tractor['dec']*u.degree)
    c2 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle
    idx[~w] = -1
    idx1 = np.where(w)[0]
    idx2 = idx[idx>-1]
    distance = d2d.value[w]
    tc = tractor[idx1]
    sm = sim[idx2]

    tab = hstack((Table(tc),Table(sm)))
    tab.rename_column('ra_1', 'ra')
    tab.rename_column('dec_1', 'dec')
    
    c1 = SkyCoord(ra=tab['ra']*u.degree, dec=tab['dec']*u.degree)
    c2 = SkyCoord(ra=original_sim['ra']*u.degree,dec = original_sim['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w = d2d.value <= angle

    #add redshift to elgs
    new_tab = tab 
    origin_sim_tab = original_sim[idx] #origin_sim_tab = original_sim[idx2]
    redshift = origin_sim_tab['nn_redshift']
    redshift[~w]=-1
    final_tab = hstack((new_tab,Table([redshift],names=('nn_redshift',))))
    
    #processing on sim, add redshift/recover or not/fracin in data column/is elg not not/ to sim file
    c1 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    c2 = SkyCoord(ra=original_sim['ra']*u.degree,dec = original_sim['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    redshift = original_sim[idx]['nn_redshift'] #redshift information
    ##
    #import pdb;pdb.set_trace()
    original_tractor = fits.getdata(fn_tractor)
    c1 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    c2 = SkyCoord(ra=original_tractor['ra']*u.degree,dec = original_tractor['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w_recover = d2d.value <= angle #recovered sources
    fracin_g = original_tractor[idx]['fracin_g']
    fracin_r = original_tractor[idx]['fracin_r']
    fracin_z = original_tractor[idx]['fracin_z']
    Type = original_tractor[idx]['type']
    flux_g = original_tractor[idx]['flux_g']
    flux_r = original_tractor[idx]['flux_r']
    flux_z = original_tractor[idx]['flux_z']
    flux_ivar_g = original_tractor[idx]['flux_ivar_g']
    flux_ivar_r = original_tractor[idx]['flux_ivar_r']
    flux_ivar_z = original_tractor[idx]['flux_ivar_z']
    mw_transmission_g = original_tractor[idx]['mw_transmission_g']
    mw_transmission_r = original_tractor[idx]['mw_transmission_r']
    mw_transmission_z = original_tractor[idx]['mw_transmission_z']
    brickname = original_tractor[idx]['brickname']
    shapeexp_r = original_tractor[idx]['shapeexp_r']
    shapedev_r = original_tractor[idx]['shapedev_r']
    anymask_g = original_tractor[idx]['anymask_g']
    anymask_r = original_tractor[idx]['anymask_r']
    anymask_z = original_tractor[idx]['anymask_z']
    allmask_g = original_tractor[idx]['allmask_g']
    allmask_r = original_tractor[idx]['allmask_r']
    allmask_z = original_tractor[idx]['allmask_z']
    shapeexp_e1_ivar = original_tractor[idx]['shapeexp_e1_ivar']
    shapeexp_e2_ivar = original_tractor[idx]['shapeexp_e2_ivar']
    shapeexp_r_ivar = original_tractor[idx]['shapeexp_r_ivar']
    shapedev_r_ivar = original_tractor[idx]['shapedev_r_ivar']
    shapedev_e1_ivar = original_tractor[idx]['shapedev_e1_ivar']
    shapedev_e2_ivar = original_tractor[idx]['shapedev_e2_ivar']
    ##
    c1 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    c2 = SkyCoord(ra=final_tab['ra']*u.degree, dec=final_tab['dec']*u.degree)
    idx, d2d, d3d = c1.match_to_catalog_sky(c2)
    w_elg = d2d.value <= angle #is elg nor not
 
    extra_tab = Table([w_recover,redshift,w_elg,fracin_g,fracin_r,fracin_z,Type,flux_g,flux_r,flux_z,flux_ivar_g,flux_ivar_r,flux_ivar_z,mw_transmission_g,mw_transmission_r,mw_transmission_z,brickname,shapeexp_r,shapedev_r,anymask_g,anymask_r,anymask_z,allmask_g,allmask_r,allmask_z,shapeexp_e1_ivar,shapeexp_e2_ivar,shapeexp_r_ivar,shapedev_r_ivar,shapedev_e1_ivar,shapedev_e2_ivar],names=('recovered','redshift','is_elg','fracin_g','fracin_r','fracin_z','type','flux_g','flux_r','flux_z','flux_ivar_g','flux_ivar_r','flux_ivar_z','mw_transmission_g','mw_transmission_r','mw_transmission_z','brickname','shapeexp_r','shapedev_r','anymask_g','anymask_r','anymask_z','allmask_g','allmask_r','allmask_z','shapeexp_e1_ivar','shapeexp_e2_ivar','shapeexp_r_ivar','shapedev_r_ivar','shapedev_e1_ivar','shapedev_e2_ivar'))
    sim_tab = Table.read(fn_sim)
    sim_tab = hstack((sim_tab,extra_tab))
    return final_tab,Table(sim_tab)


def production_run_general_perbrick_w_bricklist(bricklist = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/brickstat/elg_kaylan_run/bricks_extra.txt'):
    bricknames = np.loadtxt(bricklist,dtype=np.str)
    ttable = None
    sim_table = None
    from astropy.table import vstack
    for brickname in bricknames:
        print(brickname)
        tab,sim = production_run_general_perbrick(brickname,'my_ngc_run','more_rs0','ngc')
        if ttable is None:
            ttable = tab
            sim_table = sim
        else:
            if tab is not None:
                ttable = vstack((ttable,tab))
                sim_table = vstack((sim_table,sim))
    ttable.write('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/extra_obiwan.fits')
    sim_table.write('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/extra_sim.fits')
def nn_redshift_match(dat):
    #returns matched redshift of data
    brickname = dat['brickname']
    sim_id = dat['sim_id']
    sim_fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/ngc_brick_dat/brick_'+brickname+'.fits'
    sim_dat = fits.getdata(sim_fn)[:93]
    sim_match = sim_dat[sim_dat['id']==sim_id]
    assert(len(sim_match)==1)
    return sim_match[0]['nn_redshift']

def my_ngc_run():
    #wrap of my_NGC_run_perbrick
    import glob
    from astropy.table import vstack
    paths = glob.glob(os.path.join(os.environ['my_ngc_run'],'tractor','*','*'))
    final_tab = None
    final_sim = None
    for path in paths:
        brickname = os.path.basename(path)
        print(brickname)
        tab,sim = my_NGC_run_perbrick(brickname)
        if tab is not None:
            if final_tab is None:
                 final_tab=tab
                 final_sim=sim
            else:
               final_tab = vstack((final_tab,tab))
               final_sim = vstack((final_sim,sim))
    final_tab.write(os.path.join(os.environ['obiwan_out'],'subset','my_ngc_run_obiwan.fits'), format='fits',overwrite=True)
    final_sim.write(os.path.join(os.environ['obiwan_out'],'subset','my_ngc_run_sim.fits'), format='fits',overwrite=True)


def NGC_match():
    #calling NGC_match_perbrick
    import glob
    from astropy.table import vstack
    paths = glob.glob(os.path.join(os.environ['NGC_tractor'],'*','*'))
    final_tab = None
    for path in paths:
        brickname = os.path.basename(path)
        print(brickname)
        tab = NGC_match_perbrick(brickname)
        if tab is not None:
            if final_tab is None:
                 final_tab=tab
            else:
               final_tab = vstack((final_tab,tab))
    final_tab.write(os.path.join(os.environ['obiwan_out'],'subset','NGC_match.fits'), format='fits',overwrite=True)   

def NGC_bricklist():
    #write names for kaylan's finished bricks
    import glob
    paths = glob.glob(os.path.join(os.environ['NGC_tractor'],'*','*'))
    f = open(os.path.join(os.environ['NGC_tractor'],'bricklist_ngc.txt'),'w')
    for path in paths:
        brickname = os.path.basename(path)
        f.write(brickname+'\n')
    f.close()

def NGC_brick_select():
    #select all the bricks that are in ngc region
    fn = os.path.join(os.environ['NGC_tractor'],'bricklist_ngc.txt')
    bricknames = np.loadtxt(fn,dtype=np.str)
    fn2 = os.path.join(os.environ['NGC_tractor'],'bricklist_real_ngc.txt')
    f = open(fn2,'w')
    for brickname in bricknames:
        if brickname[4]=='p' and int(brickname[5:])>=100:
             f.write(brickname+'\n')
    f.close()

def ELG_selection_for_dr3(brickname,region='sgc'):
    print(brickname)
    try:
        tractor = fits.getdata(os.path.join(dr3_tractor_dir,brickname[:3],'tractor-'+brickname+'.fits'))
    except:
        print('NOTICE:brick %s does not exist' %brickname)
        return False,None
    # opens the tractor file
    #hdu=fits.open(path_2_tractor_file)
    #dat=hdu[1].data
    #hdu.close()

    noJunk = (tractor['brick_primary'])&(tractor['decam_anymask'][:,1]==0)&(tractor['decam_anymask'][:,2]==0)&(tractor['decam_anymask'][:,4]==0)&(tractor['tycho2inblob']==False)
    value_g=tractor['decam_depth'][:,1]
    value_r=tractor['decam_depth'][:,2]
    value_z=tractor['decam_depth'][:,4]
    gL = 62.79716079 
    rL = 30.05661087
    zL_ngc = 11.0
    zL_sgc = 12.75  
    depth_selection_ngc = (value_g > gL) & (value_r > rL) & (value_z > zL_ngc)
    depth_selection_sgc = (value_g > gL) & (value_r > rL) & (value_z > zL_sgc)
    
    # the color color selection
    g     = 22.5 - 2.5 * n.log10(tractor['decam_flux'][:,1] / tractor['decam_mw_transmission'][:,1])
    r_mag = 22.5 - 2.5 * n.log10(tractor['decam_flux'][:,2] / tractor['decam_mw_transmission'][:,2])
    z_mag = 22.5 - 2.5 * n.log10(tractor['decam_flux'][:,4] / tractor['decam_mw_transmission'][:,4])
    gr = g - r_mag
    rz = r_mag - z_mag
    color_sgc = (g>21.825)&(g<22.825)&(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.218*gr+0.571<rz)&(rz<-0.555*gr+1.901)
    color_ngc = (g>21.825)&(g<22.9)  &(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.637*gr+0.399<rz)&(rz<-0.555*gr+1.901)
    # final selection boolean array :
    selection_sgc =(noJunk)&(color_sgc)&(depth_selection_sgc)
    selection_ngc =(noJunk)&(color_ngc)&(depth_selection_ngc)
    if region == 'sgc':
        if len(selection_sgc.nonzero()[0])>0:
            flag = True
            return flag, Table(tractor[selection_sgc.astype(bool)])
        else:
            flag = False
            return flag, Table(tractor[selection_sgc.astype(bool)])
    if region == 'ngc':
            if len(selection_ngc.nonzero()[0])>0 :
                flag = True
                return flag, Table(tractor[selection_ngc.astype(bool)])
            else:
                flag = False
                return flag, Table(tractor[selection_ngc.astype(bool)])   

            
def ELG_like_selection_for_dr3(brickname,region='sgc'):
    print(brickname)
    try:
        tractor = fits.getdata(os.path.join(dr3_tractor_dir,brickname[:3],'tractor-'+brickname+'.fits'))
    except:
        print('NOTICE:brick %s does not exist' %brickname)
        return False,None
    # opens the tractor file
    #hdu=fits.open(path_2_tractor_file)
    #dat=hdu[1].data
    #hdu.close()

    noJunk = (tractor['brick_primary'])&(tractor['decam_anymask'][:,1]==0)&(tractor['decam_anymask'][:,2]==0)&(tractor['decam_anymask'][:,4]==0)&(tractor['tycho2inblob']==False)
    value_g=tractor['decam_depth'][:,1]
    value_r=tractor['decam_depth'][:,2]
    value_z=tractor['decam_depth'][:,4]
    gL = 62.79716079 
    rL = 30.05661087
    zL_ngc = 11.0
    zL_sgc = 12.75  
    depth_selection_ngc = (value_g > gL) & (value_r > rL) & (value_z > zL_ngc)
    depth_selection_sgc = (value_g > gL) & (value_r > rL) & (value_z > zL_sgc)
    
    # the color color selection
    g     = 22.5 - 2.5 * n.log10(tractor['decam_flux'][:,1] / tractor['decam_mw_transmission'][:,1])
    r_mag = 22.5 - 2.5 * n.log10(tractor['decam_flux'][:,2] / tractor['decam_mw_transmission'][:,2])
    z_mag = 22.5 - 2.5 * n.log10(tractor['decam_flux'][:,4] / tractor['decam_mw_transmission'][:,4])
    gr = g - r_mag
    rz = r_mag - z_mag
    color_sgc = (g>21.0)&(g<23.2)&(-0.068*rz+0.457<gr+0.3)&(0.112*rz+0.773>gr-0.2) &(0.218*gr+0.571<rz+0.3)&(rz-0.3<-0.555*gr+1.901)
    color_ngc = (g>21.0)&(g<23.2)  &(-0.068*rz+0.457<gr+0.3)&(gr-0.2< 0.112*rz+0.773) &(0.637*gr+0.399<rz+0.3)&(rz-0.3<-0.555*gr+1.901)
    # final selection boolean array :
    selection_sgc =(noJunk)&(color_sgc)&(depth_selection_sgc)
    selection_ngc =(noJunk)&(color_ngc)&(depth_selection_ngc)
    if region == 'sgc':
        if len(selection_sgc.nonzero()[0])>0:
            flag = True
            return flag, Table(tractor[selection_sgc.astype(bool)])
        else:
            flag = False
            return flag, Table(tractor[selection_sgc.astype(bool)])
    if region == 'ngc':
            if len(selection_ngc.nonzero()[0])>0 :
                flag = True
                return flag, Table(tractor[selection_ngc.astype(bool)])
            else:
                flag = False
                return flag, Table(tractor[selection_ngc.astype(bool)])            
            
            
def data_footprint_cutter():
    #fn_PB = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/collect/dr3_bricks.txt'
    fn_PB = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_200per_run/FinishedBricks.txt'
    topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
    data_file = topdir + 'eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk21.fits'
    print(data_file)
    import os
    import astropy.io.fits as fits
    import numpy as np
    bn = os.path.basename(data_file)
    output_fn = data_file[:-5]+'_200per_matched.fits'
    dat_PB = np.loadtxt(fn_PB,dtype=np.str)

    dat = fits.open(data_file)[1].data[::]
    dat = fits.BinTableHDU.from_columns(fits.ColDefs(np.array(dat))).data
    #print len(dat)
    flag = np.zeros(len(dat),dtype = bool)
    for i in range(len(dat)):
        if dat['brickname'][i] in dat_PB:
              flag[i]=True
    dat_sel = np.array(dat[flag])
    fits.BinTableHDU.from_columns(fits.ColDefs(dat_sel)).writeto(output_fn,overwrite=True)
    print(output_fn)

#if __name__=='__main__':
def nn_redshit_match_all():
    #data_footprint_cutter()
    #production_run_general_perbrick(brickname='3598p017', env_dir='dr3_tractor_data', rs_type='dr3', region='sgc', sel_func = 'ELG_selection_for_dr3',angle = 1.5/3600)
    #ELG_selection_for_dr3(brickname='0173p020')
    fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/my_ngc_run_obiwan_really_masked_chunk23.fits'
    from astropy.table import Table,hstack
    dat = Table.read(fn)
    z_list = []
    for i in range(len(dat)):
         print(i)
         z = nn_redshift_match(dat[i])
         z_list.append(z)
    z_array = np.array(z_list)
    t = Table(fits.BinTableHDU.from_columns(fits.ColDefs([fits.Column(name='nn_redshift',format='D',array=z_array)])).data)
    new_tab = hstack((dat,t))
    new_tab.write('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/my_ngc_run_obiwan_really_masked_chunk23_w_z.fits',overwrite = True)


def production_run_general_perbrick_sim(brickname, env_dir, rs_type, region ,angle = 1.5/3600):
    #collection of a production run, returns a table of ELGs, a table of sim
    fn_tractor = os.path.join(os.environ[env_dir],'tractor',brickname[:3],brickname,rs_type,'tractor-%s.fits' %brickname)
    fn_sim = os.path.join(os.environ[env_dir],'obiwan',brickname[:3],brickname,rs_type,'simcat-elg-%s.fits' %brickname)
    tractor = fits.getdata(fn_tractor)
    sim = fits.getdata(fn_sim)
    c1 = SkyCoord(ra=tractor['ra']*u.degree, dec=tractor['dec']*u.degree)
    c2 = SkyCoord(ra=sim['ra']*u.degree, dec=sim['dec']*u.degree)
    idx, d2d, d3d = c2.match_to_catalog_sky(c1)
    w = d2d.value <= angle
    tc = tractor[idx]
    sm = sim
    tab = Table([tc['ra'],tc['dec'],tc['flux_g'],tc['flux_r'],tc['flux_z'],tc['mw_transmission_g'],tc['mw_transmission_r'],tc['mw_transmission_z'],tc['fracdev'],tc['shapeexp_r'],tc['shapedev_r'],tc['shapeexp_e1'],tc['shapeexp_e2'],tc['shapedev_e1'],tc['shapedev_e2'],sm['id'],sm['gflux'],sm['rflux'],sm['zflux'],sm['mw_transmission_g'],sm['mw_transmission_r'],sm['mw_transmission_z'],sm['rhalf'],sm['n'],sm['e1'],sm['e2'],tc['brickname'],tc['psfdepth_g'],tc['psfdepth_r'],tc['psfdepth_z'],w],names=('ra','dec','flux_g','flux_r','flux_z','mw_transmission_g','mw_transmission_r','mw_transmission_z','fracdev','shapeexp_r','shapedev_r','shapeexp_e1','shapeexp_e2','shapedev_e1','shapedev_e2','sim_id','sim_gflux','sim_rflux','sim_zflux','sim_mw_transmission_g','sim_mw_transmission_r','sim_mw_transmission_z','sim_rhalf','sim_n','sim_e1','sim_e2','brickname','psfdepth_g','psfdepth_r','psfdepth_z','matched'))
    return tab, None


#production_run_general_perbrick_official('1404p140','elg_ngc_run','more_rs201','ngc',startid=201,nobj=101,name_for_randoms='ngc_randoms_per_brick')
