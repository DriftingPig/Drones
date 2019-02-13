'''
split the files into multiple piece to run parelle angular correlation function
'''
from file_system import *
import numpy as np
import healpy as hp
from astropy.table import Table
from astropy.io import fits
from math import *
from subprocess import call
def radec2thphi(ra,dec):
        return (-dec+90.)*pi/180.,ra*pi/180.
    
def ranHelpsort(filename,res=256,rad=''):
    if filename == names.rawdata_random:
        origin_dat = np.array(fits.open(filename)[1].data)[::2]
        origin_dat = fits.BinTableHDU.from_columns(fits.ColDefs(origin_dat)).data
    else:
        origin_dat = fits.open(filename)[1].data
        origin_dat = fits.BinTableHDU.from_columns(fits.ColDefs(origin_dat)).data
    npix = 12*res**2
    angm = 1.
    if rad == 'rad':
        angm = 180./pi
    pixls=np.zeros(len(origin_dat))
    print(len(origin_dat))
    try:
        ra,dec = origin_dat['ra'],origin_dat['dec']
    except:
        ra,dec = origin_dat['RA'],origin_dat['DEC']
    pixls = hp.pixelfunc.ang2pix(res,ra,dec,nest = False,lonlat = True)  
    print('done')
    orig_cols = origin_dat.columns
    pixls = np.array(pixls)
    new_cols = fits.ColDefs([
            fits.Column(name='pixl',format='I',
                        array=pixls)
                        ])
    tb_hdu = fits.BinTableHDU.from_columns(orig_cols+new_cols)
    tb_dat = Table.read(tb_hdu)
    tb_dat.sort('pixl')
    return tb_dat

#generate txt files which inculde sin, cos of ra,dec
def SprtFile_nest(filename, total_subs,res=256,rad='', use_weight = False):
    dat = ranHelpsort(filename,res,rad)
    import os
    base_filename = os.path.basename(filename)
    files = []
    for i in range(0,total_subs):
        sub_filename = base_filename[:-5]+'_subset'+str(i)+'.dat'
        f = open(os.path.join(output_filename,sub_filename),'w')
        files.append(f)
    
    sub_num = int(len(dat)/total_subs)
    count = 0
    j=0
    pixflag=[]
    for i in range(0,len(dat)):
        try:
           ra = dat['ra'][i]
           dec = dat['dec'][i]
        except:
           ra = dat['RA'][i]
           dec = dat['DEC'][i]
        thi = dec*pi/180.
        phi = ra*pi/180.
        #weight = dat['WEIGHT_SYSTOT'][i]
        #assert(weight>=0)
        #assert(weight<=1)
        if use_weight == True:
            weight = 1
            files[j].write(str(sin(thi))+' '+str(cos(thi))+' '+str(sin(phi))+' '+str(cos(phi))+' '+str(weight)+'\n')
        else:
            files[j].write(str(sin(thi))+' '+str(cos(thi))+' '+str(sin(phi))+' '+str(cos(phi))+' 1\n')
        if j != total_subs-1:
            count+=1
            if count == sub_num:
                pixflag.append(dat['pixl'][i])
                j+=1
                count=0
    for i in range(0,total_subs):
        files[i].close()
    return pixflag

def SprtFile_nest_dat(filename, total_subs, pixflag, res=256,rad='',use_weight = False):
    dat = ranHelpsort(filename,res,rad)
    import os
    base_filename = os.path.basename(filename)
    files = []
    for i in range(0,total_subs):
        sub_filename = base_filename[:-5]+'_subset'+str(i)+'.dat'
        f = open(os.path.join(output_filename,sub_filename),'w')
        files.append(f)
    
    sub_num = len(dat)/total_subs
    count = 0
    j=0
    for i in range(0,len(dat)):
        try:
           ra = dat['ra'][i]
           dec = dat['dec'][i]
        except:
           ra = dat['RA'][i]
           dec = dat['DEC'][i]
        thi = dec*pi/180.
        phi = ra*pi/180.
        if use_weight == True:
            weight = dat['WEIGHT_SYSTOT'][i]
            files[j].write(str(sin(thi))+' '+str(cos(thi))+' '+str(sin(phi))+' '+str(cos(phi))+' '+str(weight)+'\n')
        else:
            files[j].write(str(sin(thi))+' '+str(cos(thi))+' '+str(sin(phi))+' '+str(cos(phi))+' 1\n')
        #files[j].write(str(thi)+' '+str(phi)+'\n')
        if j != total_subs-1:
            count+=1
            if dat['pixl'][i] > pixflag[j] :
                j+=1
                print(count)
                count=0
    for i in range(0,total_subs):
        files[i].close()

import sys
work_name = sys.argv[1]
Type = sys.argv[2]
func_name = sys.argv[3]
dirs = surveyname(work_name,Type)
func_name = 'dirs.'+func_name
func = eval(func_name)
func()
names = survey(dirs)
output_filename = names.splitfile_dir
if Type == 'obiwan' and names.weight == True:
    pix_flag = SprtFile_nest(names.rawdata_random,20,use_weight = True)
else:
    pix_flag = SprtFile_nest(names.rawdata_random,20,use_weight = False)
if Type == 'obiwan' and names.weight == True:
      SprtFile_nest_dat(names.rawdata_data,20,pix_flag,use_weight = True)
else:
      SprtFile_nest_dat(names.rawdata_data,20,pix_flag,use_weight = False)
