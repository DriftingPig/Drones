import astropy.io.fits as fits
import numpy as np
import sys
from astropy.table import Table
#name_for_run = sys.argv[1]
#chunk = sys.argv[2]
#topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
#fn1 = topdir + '%s_%s_masked.fits'%(name_for_run,chunk)
#fn2 = topdir + 'sim_%s_%s_masked.fits'%(name_for_run,chunk)
#fns = [fn1,fn2]
chunk='chunk21'
fns = ['/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/10deg2_masked.fits']
def chunk2n(chunk_num):
    if chunk_num=='chunk21':
       return 1
    if chunk_num=='chunk22':
       return 2
    if chunk_num=='chunk23':
       return 4
    if chunk_num=='chunk25':
       return 8
for fn in fns:
    dat = fits.open(fn)[1].data
    dat_sel = dat['MCHUNK']
    dat_sel2 = dat['VETOMASK']
    sel = (dat_sel==chunk2n(chunk))&(dat_sel2==1)
    dat0=dat[sel]
    dat0 = Table(dat0)
    dat0.write(fn.replace('masked','really_masked'),overwrite = True)
    print(fn.replace('masked','really_masked'))
