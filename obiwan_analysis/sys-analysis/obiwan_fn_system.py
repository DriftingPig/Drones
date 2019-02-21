import astropy.io.fits as fits
import os
import glob
import numpy as np
import pymangle
import subprocess
#input files
class survey():
    def __init__(self,surveyname):#eg. surveynames.eboss()
        self.obiwan = surveyname.obiwan
        self.uniform = surveyname.uniform
        self.data = surveyname.data
        self.dir = surveyname.dir
    def get_obiwan(self):
        hdu = fits.open(self.obiwan)
        dat = hdu[1].data
        hdu.close()
        ObiwanMask = dat['obiwan_mask']
        Selection = (ObiwanMask%128==1)
        obiwan_dat = np.array(dat[Selection])
        print('obiwan:'+str(len(obiwan_dat)))
        return obiwan_dat
    def get_data(self):
        hdu = fits.open(self.data)
        dat=hdu[1].data
        hdu.close()
        print(dat.dtype.names)
        print('data:'+str(len(dat)))
        return dat
    def get_uniform(self):
        hdu = fits.open(self.uniform)
        dat=hdu[1].data
        hdu.close()
        print('uniform:'+str(len(dat))) 
        return dat
    def get_part_unifrom(self,sep):
        hdu=fits.open(self.uniform)
        dat=hdu[1].data[::sep]
        hdu.close()
        print('part uniform:'+str(len(dat)))
        return np.array(dat)
    def get_mock(self,ID):
        hdu=fits.open(self.data)
        dat = hdu[1].data
        hdu.close()
        MOCKID=dat['mockid']
        SEL_MOCKID=(MOCKID==int(ID))
        dat_final = dat[SEL_MOCKID]
        print('mock:'+str(len(dat_final)))
        return np.array(dat_final)
    def get_masked_uniform(self):#tractor_anymask for obiwan
        hdu = fits.open(self.uniform)
        dat=hdu[1].data
        hdu.close()
        MKg = dat['tractor_anymask_g']
        MKr = dat['tractor_anymask_r']
        MKz = dat['tractor_anymask_z']
        MK = (MKg==False) & (MKr==False) & (MKz==False)
        dat_m = dat[MK]
        print('uniform:'+str(len(dat)))
        print('anymasked uniform:'+str(len(dat_m)))
        return np.array(dat_m)

class surveynames():
    def __init__(self):
        self.dir = ''
        self.obiwan = ''
        self.uniform = ''
        self.data = ''
        self.comment = ''
        self.star_map = '/global/homes/h/huikong/eboss/LSSanalysis/maps/allstars17.519.9Healpixall256.dat'
        self.ext_map = '/global/homes/h/huikong/eboss/LSSanalysis/maps/healSFD_r_256_fullsky.dat'
        self.anand_map = '/global/homes/h/huikong/eboss/LSSanalysis/maps/ELG_hpsyst.nside256.fits'
    def eboss(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'randoms_subset.fits'
        self.uniform = self.dir+'randoms_subset.fits'
        self.data = self.dir+'eBOSS_ELG_full_ALL_v1_1.dat.fits'
    def eboss_step2(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_masked_050718.fits'
        self.uniform = self.dir+'uniform_masked_050718.fits'
        self.data = self.dir+'data_masked_050718.fits'
        self.comment = 'obiwan_mask.py: vetomask and footprint mask (for eboss23)'
    def eboss_step3(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_step3.fits'
        self.uniform = self.dir+'uniform_step3.fits'
        self.data = self.dir+'data_step3.fits'
        self.comment='obiwan_bricks.py: cut the bricks to make three files consistent'
    def eboss_step3_anymask(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_step3_anymask.fits'
        self.uniform = self.dir+'uniform_step3_anymask.fits'
        self.data = self.dir+'data_step3_anymask.fits'
        self.comment='obiwan_bricks.py: cut the bricks to make three files consistent with uniform has anymask'
    def eboss_step4(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_step4.fits'
        self.uniform = self.dir+'uniform_step4.fits'
        self.data = self.dir+'data_step4.fits'
        self.comment='after elg selection, processed in file ELG_selection.py'
    def eboss_step5(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_step4.fits'
        self.uniform = self.dir+'uniform_step5.fits'
        self.data = self.dir+'data_step4.fits'
        self.comment='write weights to the uniform randoms'
    def eboss_new(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'randoms_subset.fits'
        self.uniform = self.dir+'eBOSS_ELG_full_ALL_v1_1.ran.fits'
        self.data = self.dir+'eBOSS_ELG_full_ALL_v1_1.dat.fits'
    def eboss_new_step2(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_new_step1.fits'
        self.uniform = self.dir+'uniform_new_step1.fits'
        self.data = self.dir+'data_new_step1.fits'
    def eboss_new_step3(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_step3.fits'
        self.uniform = self.dir+'uniform_step3.fits'
        self.data = self.dir+'data_step3.fits'
    def eboss_new_step4(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
        self.obiwan = self.dir+'obiwan_new_step4.fits'
        self.uniform = self.dir+'uniform_step3.fits'
        self.data = self.dir+'data_new_step4.fits'
    def eboss_mock(self):
        self.dir = "/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/mock/"
        self.obiwan = ""
        self.uniform = self.dir+"all_qpm_elg_rands.eboss23.fits"
        self.data = self.dir+"all_qpm_elg_mocks.eboss23.fits"
    def eboss_sgc(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
        self.obiwan = self.dir + 'random_subset.fits'
        self.uniform = self.dir + 'sim_subset.fits'
        self.data = self.dir + 'dr5cat_subset.fits'
        self.comment = "newly processed sgc data"
    def eboss_sgc_masked(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
        self.obiwan = self.dir + 'randoms_subset_masked.fits'
        self.data = self.dir + 'dr5_subset_masked.fits'
        self.uniform = self.dir + 'sim_subset_masked.fits'
        self.comment = "newly processed masked sgc data"
    def eboss_sgc_masked_old(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
        self.obiwan = self.dir + 'randoms_subset_masked_old.fits'
        self.data = self.dir + 'dr5_subset_masked_old.fits'
        self.uniform = self.dir + 'sim_subset_masked_old.fits'
        self.comment = "newly processed masked sgc data"
    def eboss_WEIGHT_SYSTOT_sub(self):
        self.dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_data/'
        self.data = self.dir+'eBOSS_ELG_full_ALL_v1_1.dat_sub.fits'
        self.uniform = self.dir+'eBOSS_ELG_full_ALL_v1_1.ran_sub.fits'
#mask
class masks():
    def __init__(self):
        self.maskdir = ''
        self.vetomask = []
        self.footmask = []
    def eboss23(self):
        self.maskdir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/mask/eboss/'
        self.init_eboss_vetomask()
        self.init_eboss23_mask()
    def init_eboss_vetomask(self):
        eboss_mask = glob.glob(self.maskdir+'*eboss*')
        all_mask = glob.glob(self.maskdir+'*')
        veto_mask = np.array(list(set(all_mask)-set(eboss_mask)))
        self.vetomask = veto_mask
    def init_eboss23_mask(self):
        eboss_mask23 = glob.glob(self.maskdir+'*eboss23*')
        self.footmask.append(eboss_mask23[0])
        
def mask(inl,maskl,md='veto',upper = True):
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
    

#mask the data    
def mask_survey(SURVEYNAME,TYPE,output_name,upper = True):
    if SURVEYNAME == 'eboss23':
        eboss = surveynames()
        eboss.eboss()
        eboss_survey = survey(eboss)
        if TYPE == 'obiwan':
            survey_dat = eboss_survey.get_obiwan()
	#    print('obiwan:'+str(len(survey_dat)))
        elif TYPE == 'uniform':
            survey_dat = eboss_survey.get_uniform()
	 #   print ('uniform:'+str(len(survey_dat)))
        elif TYPE == 'data':
            survey_dat = eboss_survey.get_data()
	  #  print('data:'+str(len(survey_dat)))
        else:
            raise ValueError('ERROR01!')
        survey_mask = masks()
        survey_mask.eboss23()
    elif SURVEYNAME == 'eboss23_new':
        eboss = surveynames()
        eboss.eboss_new()
        eboss_survey = survey(eboss)
        if TYPE == 'obiwan':
                survey_dat = eboss_survey.get_obiwan()
        elif TYPE == 'uniform':
                survey_dat = eboss_survey.get_uniform()
        elif TYPE == 'data':
                survey_dat = eboss_survey.get_data()
        survey_mask = masks()
        survey_mask.eboss23()
    else:
        raise ValueError('ERROR02!')
        return False
    
    
    dat_vetol = mask(survey_dat,survey_mask.vetomask,'veto',upper)
    dat_footl = mask(survey_dat,survey_mask.footmask,'foot',upper)
    col_dat_vetol = fits.Column(name='veto_mask', format='B', array = dat_vetol)
    col_dat_footl = fits.Column(name='foot_mask', format='B', array = dat_footl)
    col_dat_orig = fits.ColDefs(np.array(survey_dat))
    col_dat_mask = col_dat_orig.add_col(col_dat_vetol).add_col(col_dat_footl)
    dat_temp = fits.BinTableHDU.from_columns(col_dat_mask).writeto('./temp.fits',overwrite = True)
    dat_masked = fits.open('./temp.fits')[1].data
    subprocess.call(["rm","temp.fits"])
    mask1 = dat_masked['veto_mask']
    mask2 = dat_masked['foot_mask']
    if upper:
        DEC = 'DEC'
    else:
        DEC = 'dec'
    mask_dec = dat_masked[DEC]
    mask_sel = (mask1==True) & (mask2==True) & (mask_dec>14.05)
    dat_final = np.array(dat_masked[mask_sel])
    print(len(dat_final),len(dat_masked),len(survey_dat))
    fits.BinTableHDU.from_columns(fits.ColDefs(np.array(dat_final))).writeto(output_name,overwrite=True)
    
def eboss23_mask_main():
    out_dir = '/global/cscratch1/sd/huikong/obiwan_data/data_from_obiwantest/obiwan_test/obiwan_corr/data/rawdata/randoms_eboss_041118/'
    mask_survey('eboss23','obiwan',out_dir+'obiwan_masked_050718.fits',upper = False)
    mask_survey('eboss23','uniform',out_dir+'uniform_masked_050718.fits',upper = False)
    mask_survey('eboss23','data',out_dir+'data_masked_050718.fits',upper = True)
    
#eboss23_mask_main()

def file_output(data_array,file_name):
	fits.BinTableHDU.from_columns(fits.ColDefs(np.array(data_array))).writeto(file_name,overwrite=True)	

def add_column(data_set,extra_col,col_name,col_format):
	col_orig = fits.ColDefs(np.array(data_set))
	col_added = fits.Column(name=col_name, format=col_format, array = extra_col)
	col_final = col_orig.add_col(col_added)
	dat_temp = fits.BinTableHDU.from_columns(col_final).writeto('./temp.fits',overwrite = True)
	dat_final = fits.open('./temp.fits')[1].data
	subprocess.call(["rm","temp.fits"])
	return dat_final

def add_column_with_saved_file(data_set,extra_col,col_name,col_format,output_name,mode):
        col_orig = fits.ColDefs(np.array(data_set))                                       
        col_added = fits.Column(name=col_name, format=col_format, array = extra_col)      
        col_final = col_orig.add_col(col_added)
        dat_temp = fits.BinTableHDU.from_columns(col_final).writeto(output_name,overwrite = True)
        hdu = fits.open(output_name,mode = mode)
        return hdu
