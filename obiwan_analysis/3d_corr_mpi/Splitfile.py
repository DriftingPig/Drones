import astropy.io.fits as fits
import numpy as np
import healpy as hp
import os
from astropy.table import Table
def splitfile_random(fn,output_dir,z_colname = 'nn_redshift', N=20, res = 256, random_z = False, dat_fn = None, dat_z_col='Z',use_weight=False,weight_col=[]):

    data = fits.getdata(fn)[::]
    print("sim length:")
    print(len(data))
    try:
       ra,dec = data['ra'],data['dec']
    except:
       ra,dec = data['RA'],data['DEC']
    if random_z == True:
       dat2 = fits.getdata(dat_fn)
       seed_z = dat2[dat_z_col]
       idx = np.random.randint(0,len(seed_z),size = len(data))
       z = seed_z[idx]
    else:    
       z = data[z_colname]
    if use_weight == False:
       w = np.ones(len(data))
    else:
       #import pdb
       #pdb.set_trace()
       w = np.ones(len(data))
       for item in weight_col:
            w = w*data[item]
    pixls = hp.pixelfunc.ang2pix(res,ra,dec,nest = False,lonlat = True)
    col_ra = fits.Column(name = 'ra', format='D', array = ra)
    col_dec = fits.Column(name = 'dec', format='D', array = dec)
    col_z = fits.Column(name = 'z', format='D', array = z)
    col_w = fits.Column(name = 'w', format = 'D', array = w)
    col_pixl = fits.Column(name = 'pixl', format = 'D', array = pixls)
    cols = fits.ColDefs([col_ra,col_dec,col_z,col_w, col_pixl])
    tb_hdu = fits.BinTableHDU.from_columns(cols)
    tb_dat = Table.read(tb_hdu)
    z_val = tb_dat['z']
    tb_dat = tb_dat[((z_val>0.6)&(z_val<1.1))]
    tb_dat.sort('pixl') 
    idx = np.arange(len(tb_dat))
    sub_idx = np.array_split(idx, N)
    pix_list = []
    print('sim final:='+str(len(idx)))
    n1=0;n2=0
    for i in range(N):
       pix_list.append(tb_dat['pixl'][sub_idx[i][0]])
       sub_tab = tb_dat[sub_idx[i][0]:sub_idx[i][-1]+1]
       sub_fn = os.path.basename(fn).replace('.fits','_subset'+str(i)+'.fits')
       sub_tab.write(output_dir+sub_fn,overwrite=True)
       print(len(sub_tab),sum(sub_tab['w']))
       n1+=len(sub_tab);n2+=sum(sub_tab['w'])
    print(n1,n2)
    print(len(tb_dat),sum(tb_dat['w']))
    return pix_list

def splitfile_data(fn,output_dir,pix_list,z_colname = 'Z',N=20, res = 256,use_weight=False,weight_col=[]):
    data = fits.getdata(fn)
    print('data length:')
    print(len(data))
    try:
       ra,dec = data['ra'],data['dec']
    except:
       ra,dec = data['RA'],data['DEC']
    z = data[z_colname]
    if use_weight == False:
       w = np.ones(len(data))
    else:
       print('yes**')
       w = np.ones(len(data))
       for item in weight_col:
               w = w*data[item]
    #w = np.ones(len(data))
    pixls = hp.pixelfunc.ang2pix(res,ra,dec,nest = False,lonlat = True)
    col_ra = fits.Column(name = 'ra', format='D', array = ra)
    col_dec = fits.Column(name = 'dec', format='D', array = dec)
    col_z = fits.Column(name = 'z', format='D', array = z)
    col_w = fits.Column(name = 'w', format = 'D', array = w)
    col_pixl = fits.Column(name = 'pixl', format = 'D', array = pixls)
    cols = fits.ColDefs([col_ra,col_dec,col_z,col_w,col_pixl])
    tb_hdu = fits.BinTableHDU.from_columns(cols)
    tb_dat = Table.read(tb_hdu)
    z_val = tb_dat['z']
    tb_dat = tb_dat[((z_val>0.6)&(z_val<1.1))]
    tb_dat.sort('pixl')
    pix_list.append(tb_dat['pixl'].max())
    #import pdb
    #pdb.set_trace()
    n1=0;n2=0
    for i in range(N):
        if i != N-1:
            sub_tab = tb_dat[(tb_dat['pixl']>=pix_list[i])&(tb_dat['pixl']<pix_list[i+1])]
        else:
            sub_tab = tb_dat[(tb_dat['pixl']>=pix_list[i])&(tb_dat['pixl']<=pix_list[i+1])]
        sub_fn = os.path.basename(fn).replace('.fits','_subset'+str(i)+'.fits')
        sub_tab.write(output_dir+sub_fn,overwrite=True)
        print(len(sub_tab),sum(sub_tab['w']))
        #print(output_dir+sub_fn)
        n1+=len(sub_tab);n2+=sum(sub_tab['w'])
    print(n1,n2)
    print(len(tb_dat),sum(tb_dat['w']))
    return 'DONE'

def main():
    name = 'my_ngc_run'
    Type = 'uniform'
    raw_topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
    data_name = 'eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk23_cutted.fits'
    obiwan_name = 'my_ngc_run_obiwan_really_masked_chunk23_w_z.fits'
    uniform_name = 'my_ngc_run_sim_really_masked_chunk23.fits'
    output_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/'+name+'/splitdata/'+Type+'/'
    pix_list = splitfile_random(raw_topdir+uniform_name,output_dir)
    print('1 done')
    splitfile_data(raw_topdir+data_name,output_dir,pix_list)
    print('2 done')
if __name__=='__main__':
    main()
