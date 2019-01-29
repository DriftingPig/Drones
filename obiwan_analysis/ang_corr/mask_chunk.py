#mask function defined to mask eboss ELGs:
#masks are in: https://data.sdss.org/sas/ebosswork/users/u0992342/eBOSS_ELG/ELG_masks/
mask_dir  = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/ipynb_data/'
import pymangle
import numpy as np
def mask(inl,maskl,md='veto',upper = False):
        '''
        input: inl--data, mask--file names of the mask list
        output: list of True/False for whether a point should be masked
        '''
        if upper:
            RA = 'RA'
            DEC = 'DEC'
        else:
            RA = 'ra'
            DEC = 'dec'

        if md == 'foot':
                keep = np.zeros(inl.size,dtype='bool')  #object is outside of footprint unless it is found
        if md == 'veto':
                keep = np.ones(inl.size,dtype='bool')   #object is outside of veto mask unless it is found

        for mask in maskl:
                mng = pymangle.Mangle(mask)
                polyid = mng.polyid(inl[RA],inl[DEC])
                if md == 'foot':
                        keep[polyid!=-1] = True #keep the object if a polyid is found
                if md == 'veto':
                        keep[polyid!=-1] = False #do not keep the object if a polyid is found   
                print(mask+' done')
        return keep
    
def init_eboss_mask():#chunk21,22
        '''
        generate a list of fileanmes for vetomask and footprint mask
        returns:
        veto mask list, footprint mask list
        '''
        maskdir = mask_dir 
        veto_mask = []
        veto_mask.append(maskdir+'bright_object_mask_rykoff_pix.ply')
        veto_mask.append(maskdir+'tycho2mask-0Vmag10.pol')
        veto_mask.append(maskdir+'tycho2mask-10Vmag11.pol')
        veto_mask.append(maskdir+'tycho2mask-11Vmag115.pol')
        veto_mask.append(maskdir+'ELG_centerpost.ply')
        veto_mask.append(maskdir+'ELG_bright_objstar.pix6s.snap.balk.ply')
        footprint_mask = []
        footprint_mask.append(maskdir+'geometry-eboss21.ply')
        footprint_mask.append(maskdir+'geometry-eboss22.ply')
        return veto_mask,footprint_mask
    
def init_eboss_mask_chunk21():
        '''
        generate a list of fileanmes for vetomask and footprint mask
        returns:
        veto mask list, footprint mask list
        '''
        maskdir = mask_dir 
        veto_mask = []
        veto_mask.append(maskdir+'bright_object_mask_rykoff_pix.ply')
        veto_mask.append(maskdir+'tycho2mask-0Vmag10.pol')
        veto_mask.append(maskdir+'tycho2mask-10Vmag11.pol')
        veto_mask.append(maskdir+'tycho2mask-11Vmag115.pol')
        veto_mask.append(maskdir+'ELG_centerpost.ply')
        veto_mask.append(maskdir+'ELG_bright_objstar.pix6s.snap.balk.ply')
        footprint_mask = []
        footprint_mask.append(maskdir+'geometry-eboss21.ply')
        return veto_mask,footprint_mask    

def init_eboss_mask_chunk22():
        '''
        generate a list of fileanmes for vetomask and footprint mask
        returns:
        veto mask list, footprint mask list
        '''
        maskdir = mask_dir 
        veto_mask = []
        veto_mask.append(maskdir+'bright_object_mask_rykoff_pix.ply')
        veto_mask.append(maskdir+'tycho2mask-0Vmag10.pol')
        veto_mask.append(maskdir+'tycho2mask-10Vmag11.pol')
        veto_mask.append(maskdir+'tycho2mask-11Vmag115.pol')
        veto_mask.append(maskdir+'ELG_centerpost.ply')
        veto_mask.append(maskdir+'ELG_bright_objstar.pix6s.snap.balk.ply')
        footprint_mask = []
        footprint_mask.append(maskdir+'geometry-eboss22.ply')
        return veto_mask,footprint_mask
#choose a chunk
chunk = 'chunk22'
func = eval('init_eboss_mask_'+chunk)
veto_mask,foot_mask = func()

import astropy.io.fits as fits
from file_system import *
func_name = 'TS_master_cutted'
name = func_name
dirs = surveyname(name,'uniform')
eval('dirs.'+func_name)()
s_name = survey(dirs)
random_name = s_name.rawdata_random
data_name = s_name.rawdata_data
random_dat = fits.open(random_name)[1].data
data_dat = fits.open(data_name)[1].data

'''
veto_list = mask(random_dat,veto_mask,md='veto')
foot_list = mask(random_dat,foot_mask,md='foot')
col_dat_vetol = fits.Column(name='veto_mask', format='B', array = veto_list)
col_dat_footl = fits.Column(name='foot_mask', format='B', array = foot_list)
col_dat_orig = fits.ColDefs(np.array(random_dat))
col_dat_mask = col_dat_orig.add_col(col_dat_vetol).add_col(col_dat_footl)
dat_masked = fits.BinTableHDU.from_columns(col_dat_mask).data
mask1 = dat_masked['veto_mask']
mask2 = dat_masked['foot_mask']
mask_sel = (mask1==True) & (mask2==True)
random_masked = np.array(dat_masked[mask_sel])
random_chunk = fits.ColDefs(random_masked)
t1 = fits.BinTableHDU.from_columns(random_chunk)
t1.writeto(random_name[:-5]+'_masked_chunk21.fits',overwrite=True)
print(random_name[:-5]+'_masked_chunk21.fits')

'''
veto_list = mask(data_dat,veto_mask,md='veto')
foot_list = mask(data_dat,foot_mask,md='foot')
col_dat_vetol = fits.Column(name='veto_mask', format='B', array = veto_list)           
col_dat_footl = fits.Column(name='foot_mask', format='B', array = foot_list)
col_dat_orig = fits.ColDefs(np.array(data_dat))                                      
col_dat_mask = col_dat_orig.add_col(col_dat_vetol).add_col(col_dat_footl)
dat_masked = fits.BinTableHDU.from_columns(col_dat_mask).data                          
mask1 = dat_masked['veto_mask']                                                        
mask2 = dat_masked['foot_mask']                                                        
mask_sel = (mask1==True) & (mask2==True)                                               
random_masked = np.array(dat_masked[mask_sel])
random_chunk = fits.ColDefs(random_masked)
t1 = fits.BinTableHDU.from_columns(random_chunk)
t1.writeto(data_name[:-5]+'_masked_chunk22.fits',overwrite=True)
print(data_name[:-5]+'_masked_chunk22.fits')

