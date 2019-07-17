import healpy as hp
import astropy.io.fits as fits
from astropy.table import Table,hstack
import matplotlib.pyplot as plt
import numpy as np
from file_system import *
from math import *
class pixel_conversion(object):
    '''
    give the input obwian data(with sim) a weight. 
    radec2pixdens:return pixel id; weight
    map_maker: can make a density plot of it
    weight_adder: add the weight to the a data file, output a file that has 
    '''
    def __init__(self,fn,fn_sim,res):
       self.fn = fn
       self.fn_sim = fn_sim
       self.res = res
       self.pixel_id = None
       self.weight = None
       self.ra_list = None
       self.dec_list = None
    def radec2thiphi(self,ra,dec):
        return dec*pi/180.,ra*pi/180
    def angdis(self,thi1,phi1,thi2,phi2):
        return cos(thi1)*cos(thi2)*cos(phi1-phi2)+sin(thi1)*sin(thi2)
    def find_min_angdis_id(self,ra,dec,ra_edge,dec_edge):
        """
        input:list of ra,dec,ra_edge,dec_edge
        return: the ra,dec index closest to ra_edge,dec_edge
                index is consistent with pixel_id,weight,ra_list,dec_list
        """
        thi1,phi1 = self.radec2thiphi(ra,dec)
        thi2,phi2 = self.radec2thiphi(ra_edge,dec_edge)
        min_angdis_id = []
        for i in range(len(thi2)):
            min_angdis = 10000000
            min_angdisID = -1
            for j in range(len(thi1)):
                angdis = self.angdis(thi1[j],phi1[j],thi2[i],phi2[i])
                if angdis<min_angdis:
                    min_angdisID=j
                    min_angdis=angdis
            assert(min_angdisID>=0)
            min_angdis_id.append(min_angdisID)
        return min_angdis_id
    def radec2pixdens(self):
        dat = fits.getdata(self.fn)
        sim = fits.getdata(self.fn_sim)
        npix = 12*self.res**2
        try:
           ra,dec = dat['ra'],dat['dec']
        except:
           ra,dec = dat['RA'],dat['DEC']
        try:
           ra_sim,dec_sim = sim['ra'],sim['dec']
        except:
           ra_sim,dec_sim = sim['RA'],sim['DEC']
        pixls = hp.pixelfunc.ang2pix(self.res,ra,dec,nest = False,lonlat = True) 
        pixls_sim = hp.pixelfunc.ang2pix(self.res,ra_sim,dec_sim,nest = False,lonlat = True) 
        unique_pixls = np.unique(pixls)
        unique_pixls_count = np.zeros_like(unique_pixls)
        unique_pixls_count_sim = np.zeros_like(unique_pixls)
        for i in range(len(unique_pixls)):
           unique_pixls_count[i]+=(pixls==unique_pixls[i]).sum()
           unique_pixls_count_sim[i]+=(pixls_sim==unique_pixls[i]).sum()
        unique_pixls_count_sim_cutted = unique_pixls_count_sim[unique_pixls_count_sim>unique_pixls_count_sim.max()/2.]
        unique_pixls_count_cutted = unique_pixls_count[unique_pixls_count_sim>unique_pixls_count_sim.max()/2.]
        unique_pixls_cutted = unique_pixls[unique_pixls_count_sim>unique_pixls_count_sim.max()/2.]
        weight = 1./(unique_pixls_count_cutted/unique_pixls_count_sim_cutted*(unique_pixls_count_sim_cutted.sum()/unique_pixls_count_cutted.sum()))
        #edges of unique pixels
        unique_pixls_count_sim_edge = unique_pixls_count_sim[(unique_pixls_count_sim<=unique_pixls_count_sim.max()/2.)&(unique_pixls_count_sim>0)]
        unique_pixls_count_edgc = unique_pixls_count[(unique_pixls_count_sim<=unique_pixls_count_sim.max()/2.)&(unique_pixls_count_sim>0)]
        unique_pixls_edge = unique_pixls[(unique_pixls_count_sim<=unique_pixls_count_sim.max()/2.)&(unique_pixls_count_sim>0)]
        ra,dec = hp.pixelfunc.pix2ang(self.res,unique_pixls_cutted,nest = False,lonlat = True)
        ra_edge,dec_edge = hp.pixelfunc.pix2ang(self.res,unique_pixls_edge, nest = False,lonlat = True)
        index_list = self.find_min_angdis_id(ra,dec,ra_edge,dec_edge)
        self.ra_list = ra
        self.dec_list = dec
        weight_edge = weight[np.array(index_list)]
        #output these pixels
        self.pixel_id = np.hstack((unique_pixls_cutted,unique_pixls_edge))
        self.weight = np.hstack((weight,weight_edge))
        return unique_pixls_cutted,weight

    def map_maker(self,shw_plt = False,sav_plt = True,plt_name='density_plt.png'):
        if self.pixel_id is None:
            self.radec2pixdens()
        ra,dec = hp.pixelfunc.pix2ang(self.res, self.pixel_id, nest=False, lonlat= True)
        plt.scatter(ra,dec,c = self.weight,vmin = self.weight.mean()-1.5*self.weight.std(),vmax = self.weight.mean()+1.5*self.weight.std(),marker='.')
        plt.colorbar()
        if shw_plt is True:
           plt.show()
        if sav_plt is True:
           plt.savefig('./plots/'+plt_name)
           np.savetxt('./plots/'+plt_name.replace('.png','.txt'),np.array([ra,dec,self.weight]))
    def _in_pix_list(self,fn):
        sel = []
        t = Table.read(fn)
        try:
           ra,dec = t['ra'],t['dec']
        except:
           ra,dec = t['RA'],t['DEC']
        pixls = hp.pixelfunc.ang2pix(self.res,ra,dec,nest = False,lonlat = True)
        for i in range(len(pixls)):
            if pixls[i] in self.pixel_id:
                sel.append(True)
            else:
                sel.append(False)
        return np.array(sel,dtype = np.bool)

    def weight_adder(self,fn_dat=None, fn_sim = None):
        if self.pixel_id is None:
            self.radec2pixdens()
        dat = fits.getdata(fn_dat)
        try:
          ra,dec = dat['ra'],dat['dec']
        except:
          ra,dec = dat['RA'],dat['DEC']
        pixls = hp.pixelfunc.ang2pix(self.res,ra,dec,nest = False,lonlat = True)
        obiwan_weight = []

        missinglist=[];missingpixel=[]
        for i in range(len(pixls)):
            try:
               idx = np.where(self.pixel_id == pixls[i])[0][0]
               obiwan_weight.append(self.weight[idx])
            except:
               missinglist.append(i)
               missingpixel.append(pixls[i])
               print('detect no-existence in pixel id %d'%pixls[i])
               obiwan_weight.append(0)
        ra_miss,dec_miss = hp.pixelfunc.pix2ang(self.res,np.array(missingpixel), nest = False,lonlat = True)
        ids = self.find_min_angdis_id(self.ra_list,self.dec_list,ra_miss,dec_miss)
        assert(len(ids)==len(ra_miss))
        for i in range(len(ids)):
            weight_id = missinglist[i];assert(obiwan_weight[weight_id]==0)
            obiwan_weight[weight_id] = self.weight[ids[i]]
        obiwan_weight = np.array(obiwan_weight)
        print(len(obiwan_weight),len(obiwan_weight[obiwan_weight>0]))
        assert(len(obiwan_weight)==len(obiwan_weight[obiwan_weight>0]))
        t = Table([obiwan_weight[obiwan_weight>0]], names=('obiwan_weight',),dtype = ('f4',))
        t_dat = Table.read(fn_dat)[obiwan_weight>0]
        t_final = hstack((t_dat,t))
        t_final.write(fn_dat.replace('.fits','_obiwan_weight.fits'),overwrite = True)
        print('written file as %s' %fn_dat.replace('.fits','_obiwan_weight.fits'))
        #also need to write new obiwan/sim file b/c leaving out some pixles
        if fn_sim is None:
            fn_sim = self.fn_sim
        #sim_list = self._in_pix_list(fn_sim)
        t_sim = Table.read(fn_sim)
        t_sim_weight = Table([np.ones(len(t_sim))], names = ('obiwan_weight',),dtype = ('f4',))
        t_sim = hstack((t_sim,t_sim_weight))
        t_sim.write(fn_sim.replace('.fits','_obiwan_weight.fits'),overwrite = True)
        print('written file as %s' %fn_sim.replace('.fits','_obiwan_weight.fits'))
        #obiwan_list = self._in_pix_list(self.fn)
        t_obiwan = Table.read(self.fn) #[obiwan_list]
        t_obiwan_weight = Table([np.ones(len(t_obiwan))], names = ('obiwan_weight',),dtype = ('f4',))
        t_obiwan = hstack((t_obiwan,t_obiwan_weight))
        t_obiwan.write(self.fn.replace('.fits','_obiwan_weight.fits'),overwrite = True)
        print('written file as %s' %self.fn.replace('.fits','_obiwan_weight.fits'))
        return 'success'
        
def main_plot(name,res,Type='obiwan',shw_plt=True,plt_name='density_plt.png'):
    '''
    this makes a density plot
    '''
    survey_name = surveyname(name,'obiwan')
    eval('survey_name.'+name+'()')
    assert(Type in ['obiwan','data'])
    if Type=='obiwan':
        target = pixel_conversion(survey_name.raw_topdir+survey_name.obiwan_name,survey_name.raw_topdir+survey_name.uniform_name,res)
    if Type=='data':
        target = pixel_conversion(survey_name.raw_topdir+survey_name.data_name,survey_name.raw_topdir+survey_name.uniform_name,res)
    target.map_maker(shw_plt=shw_plt,plt_name=plt_name)

def main_add_weight(name,res, fn_dat = None, fn_sim = None):
    '''
    this makes writes obiwan_weight to specified file
    '''
    survey_name = surveyname(name,'obiwan')
    eval('survey_name.'+name+'()')
    target = pixel_conversion(survey_name.raw_topdir+survey_name.obiwan_name,survey_name.raw_topdir+survey_name.uniform_name,res)
    target.weight_adder(fn_dat, fn_sim)

def main(mode,name = 'elg_ngc_run_conbimed',Type=None): 
      if mode == 1:#make plot
          main_plot(name,256,Type,shw_plt=False,plt_name='obiwan_density_chunk23.png')
      if mode == 2: #make weighted column, specify which sim file you want, because we want other weight columns for 3d corr
          fn_dat = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_clustering_eboss23_v5.dat.fits'
          fn_sim = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_clustering_eboss23_v5.ran.fits'
          main_add_weight(name,128, fn_dat,fn_sim)
main(1,name = 'elg_ngc_run_conbimed',Type='obiwan')
