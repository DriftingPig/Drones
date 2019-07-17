#making a list of real bricks with elg data files
topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
chunk21 = topdir+'eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk21.fits'
chunk22 = topdir+'eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk22.fits'
chunk23 = topdir+'eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk23.fits'
#chunk25 = TODO
import numpy as np
import astropy.io.fits as fits
def write_bricks(chunk):
    dat = fits.getdata(eval(chunk))
    bricknames_set = set(dat['brickname'])
    bricknames_array = np.array(list(bricknames_set),dtype = np.str)
    np.savetxt("real_bricks_%s.txt"%chunk,bricknames_array,fmt="%s")

write_bricks('chunk21')
write_bricks('chunk22')
write_bricks('chunk23')
