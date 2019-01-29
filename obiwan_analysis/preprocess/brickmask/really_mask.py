import astropy.io.fits as fits
import numpy as np
topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
fn1 = topdir + 'eBOSS_ELG_full_ALL_v4.dat_cutted_masked.fits'
fn2 = topdir + 'obiwan_200per_0125_masked.fits'
fns = [fn1,fn2]
for fn in fns:
    dat = fits.open(fn)[1].data
    dat_sel = dat['MCHUNK']
    dat_sel2 = dat['VETOMASK']
    sel = (dat_sel==1)&(dat_sel2==1)
    dat0=dat[sel]
    t = fits.BinTableHDU.from_columns(fits.ColDefs(np.array(dat0)))
    t.writeto(fn.replace('masked','really_masked_chunk21'),overwrite = True)
    print(fn.replace('masked','really_masked_chunk21'))
