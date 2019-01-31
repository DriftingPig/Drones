import subprocess
class survey():
      def __init__(self,surveyname):
          if surveyname.Type == 'obiwan':
                self.weight = surveyname.weight
                self.rawdata_random = surveyname.raw_topdir+surveyname.obiwan_name
                self.splitdata_random = surveyname.splitfile_topdir+surveyname.obiwan_name[:-5]+'_subset'
          else:
                self.weight = False
                self.rawdata_random = surveyname.raw_topdir+surveyname.uniform_name
                self.splitdata_random = surveyname.splitfile_topdir+surveyname.uniform_name[:-5]+'_subset'
          self.splitfile_dir = surveyname.splitfile_topdir
          self.rawdata_data = surveyname.raw_topdir+surveyname.data_name
          self.splitdata_data = surveyname.splitfile_topdir+surveyname.data_name[:-5]+'_subset'
          self.binhist = surveyname.binhist_topdir+'BinHist'
          self.binhist_topdir = surveyname.binhist_topdir
          self.totpts = surveyname.binhist_topdir+'TotalPoints.txt'
          self.corr_output = surveyname.output_topdir+surveyname.name+'_'+surveyname.Type+'.out'
          self.maps()
      def maps(self):
          self.star_map = '/global/homes/h/huikong/eboss/LSSanalysis/maps/allstars17.519.9Healpixall256.dat'
          self.ext_map = '/global/homes/h/huikong/eboss/LSSanalysis/maps/healSFD_r_256_fullsky.dat' 
          self.anand_map = '/global/homes/h/huikong/eboss/LSSanalysis/maps/ELG_hpsyst.nside256.fits'
class surveyname():
      def __init__(self,name,Type):#Type='obiwan' or 'uniform'
          self.corr_topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/'+name+'/'
          self.raw_topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
          self.splitfile_topdir = self.corr_topdir+'splitdata/'+Type+'/'
          self.binhist_topdir = self.corr_topdir+'BinHist/'+Type+'/'   
          self.output_topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/corr_output/'
          self.tractor_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/'+name+'/tractor/'
          self.Type = Type
          self.name = name      
          self.obiwan_name = ''
          self.uniform_name = ''
          self.data_name = ''
          self.name_validation = ''
          self.message = ''
          subprocess.call(["mkdir","-p",self.splitfile_topdir])
          subprocess.call(["mkdir","-p",self.binhist_topdir])
      def production_run_200per(self): 
          self.obiwan_name = 'random_subset_dr3_200per.fits'
          self.data_name = 'dr5cat_subset_dr3_200per.fits'
          self.uniform_name = 'sim_subset_dr3_200per.fits'
          self.message = 'it is dr5, 200 injections per brick using Anand ccd list'
          self.name_validation = 'elg_eboss_200per'
          self.weight = False
          assert(self.name_validation == self.name)
      def ELG_clustering_v4_chunk21(self):
          self.obiwan_name = 'eBOSS_ELG_clustering_eboss21_v4.ran.fits'
          self.data_name = 'eBOSS_ELG_clustering_eboss21_v4.dat.fits'
          self.uniform_name = 'eBOSS_ELG_clustering_eboss21_v4.ran.fits'
          self.message = "chunk21 Anand v4 version, url:https://data.sdss.org/sas/ebosswork/eboss/sandbox/lss/catalogs/versions/4/"
          self.name_validation = 'ELG_clustering_v4_chunk21'
          self.weight = True
          assert(self.name_validation == self.name)
      def ELG_clustering_v4_chunk22(self):
          self.obiwan_name = 'eBOSS_ELG_clustering_eboss22_v4.ran.fits'
          self.data_name = 'eBOSS_ELG_clustering_eboss22_v4.dat.fits'
          self.uniform_name = 'eBOSS_ELG_clustering_eboss22_v4.ran.fits'
          self.message = "chunk22 Anand v4 version, url:https://data.sdss.org/sas/ebosswork/eboss/sandbox/lss/catalogs/versions/4/"
          self.name_validation = 'ELG_clustering_v4_chunk22'
          self.weight = True
          assert(self.name_validation == self.name)
      def ELG_v4_dat_w_obiwan_chunk22(self):
          self.data_name = 'eBOSS_ELG_clustering_eboss22_v4.dat_cutted.fits'
          self.obiwan_name = 'random_subset_dr3_200per.fits'
          self.uniform_name = 'sim_subset_dr3_200per.fits'
          self.message='cut v4 elgs to the footprint processed'
          self.name_validation = 'ELG_v4_dat_w_obiwan_chunk22'
          self.weight = False
          assert(self.name_validation == self.name)
      def TS_master(self):
          self.data_name = 'ELG_TS_master.fits'
          self.weight = False
      def TS_master_cutted(self):
          self.data_name = 'ELG_TS_master_cutted.fits'
          self.obiwan_name = 'random_subset_dr3_200per_chunk22.fits'
          self.uniform_name = 'sim_subset_dr3_200per_chunk22.fits'
          self.weight = False
          self.name_validation = 'TS_master_cutted'
          assert(self.name_validation == self.name)
      def eBOSS_ELG_full_ALL_v4(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat.fits'
          self.obiwan_name = 'eBOSS_ELG_full_ALL_v4.ran.fits'
          self.uniform_name = 'eBOSS_ELG_full_ALL_v4.ran.fits'
          self.weight = True
          self.name_validation = 'eBOSS_ELG_full_ALL_v4'
          assert(self.name_validation == self.name)
      def eBOSS_ELG_full_ALL_v4_masked(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_really_masked.fits'
          self.uniform_name = 'eBOSS_ELG_full_ALL_v4.ran_really_masked.fits'
          self.obiwan_name = self.uniform_name
          self.weight = True
      def eboss_ELG_w_obiwan_masked(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_really_masked.fits'
          self.obiwan_name = 'random_subset_dr3_200per_really_masked.fits'
          self.uniform_name = 'sim_subset_dr3_200per_really_masked.fits'
          self.weight = False
      def eBOSS_ELG_full_ALL_v4_chunk22(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_chunk22.fits'
          self.obiwan_name = 'eBOSS_ELG_full_ALL_v4.ran_chunk22.fits'
          self.uniform_name = 'eBOSS_ELG_full_ALL_v4.ran_chunk22.fits'
          self.weight = True
          self.name_validation = 'eBOSS_ELG_full_ALL_v4_chunk22'
          assert(self.name_validation == self.name)
      def eboss_ELG_w_obiwan_chunk22(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_chunk22.fits'
          self.obiwan_name = 'random_subset_dr3_200per_chunk22.fits'
          self.uniform_name = 'sim_subset_dr3_200per_chunk22.fits'
          self.weight = False
      def eBOSS_ELG_full_ALL_v4_chunk22_cutted(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_chunk22_cutted.fits'
          self.obiwan_name =  'ELG.v5_11_0.rrv2.all.rands_chunk22_cutted.fits'  #'eBOSS_ELG_full_ALL_v4.ran_chunk22_cutted.fits'
          self.uniform_name = self.obiwan_name
          self.weight = True
          self.name_validation = 'eBOSS_ELG_full_ALL_v4_chunk22_cutted'
          assert(self.name_validation == self.name)
      def eBOSS_ELG_full_ALL_v4_chunk22_cutted_w_obiwan(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_chunk22_cutted.fits'
          self.obiwan_name = 'random_subset_dr3_200per_chunk22.fits'
          self.uniform_name = 'sim_randoms_gaussian_really_masked.fits'
          #'tmp_cutted.fits'   #'sim_randoms_gaussian_really_masked.fits'  #'sim_subset_dr3_200per_chunk22.fits'
          self.weight = False
          self.name_validation = 'eBOSS_ELG_full_ALL_v4_chunk22_cutted_w_obiwan'
          assert(self.name_validation == self.name)
      def obiwan_run_set2_step1(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_cutted.fits'
          self.obiwan_name = 'random_subset_dr5_200per.fits'
          self.uniform_name = 'sim_subset_dr5_200per.fits'
          self.weight = False
          self.name_validation = 'obiwan_run_set2_step1'
      def obiwan_run_set2_step2_chunk22(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_really_masked_cutted.fits'
          self.obiwan_name = 'random_subset_dr5_200per_really_masked.fits'
          self.uniform_name = 'sim_subset_dr5_200per_really_masked.fits'
          self.weight = False
          self.name_validation = 'obiwan_run_set2_step2_chunk22'
      def obiwan_run_set2_step2_chunk21(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk21_cutted.fits'
          self.obiwan_name = 'random_subset_dr5_200per_really_masked_chunk21.fits'
          self.uniform_name = 'sim_subset_dr5_200per_really_masked_chunk21.fits'
          self.weight = False
          self.name_validation = 'obiwan_run_set2_step2_chunk21'
      def obiwan_run_w_TS_chunk22(self):
          self.data_name = 'ELG_TS_master_cutted_masked_chunk22.fits'
          self.obiwan_name = 'random_subset_dr5_200per_masked.fits'
          self.uniform_name = 'sim_subset_dr5_200per_masked.fits'
          self.weight = False
      def mask_test(self):
          self.data_name = 'sim_subset_dr5_200per_really_masked.fits'
          self.obiwan_name = self.uniform_name
          self.weight = False
          self.uniform_name = 'ELG.v5_11_0.rrv2.all.rands_really_masked_chunk22_cutted.fits'
      def obiwan_200per_0125_chunk21(self):
          self.data_name = 'eBOSS_ELG_full_ALL_v4.dat_cutted_really_masked_chunk21.fits'
          self.obiwan_name = 'obiwan_200per_0125_really_masked_chunk21.fits'
          self.uniform_name = 'obiwan_200per_0125_really_masked_chunk21.fits'
          self.weight = False
      