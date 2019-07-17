surveybricks = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat_elg_like/brick_list.out'
import matplotlib.pyplot as plt
import numpy as np
'''
dat = np.loadtxt(surveybricks,dtype = np.str).transpose()
nums = np.array(dat[1],dtype=np.int)
#plt.hist(nums)
#plt.show()
f_in = open('./InsideBricks.txt','w')
f_out = open('./OutBricks.txt','w')
for i in range(len(dat[0])):
    if nums[i]>600:
       f_in.write(dat[0][i]+'\n')
    else:
       f_out.write(dat[0][i]+'\n')
'''

dat_fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk21_200per_matched.fits'
import astropy.io.fits as fits
dat = fits.open(dat_fn)[1].data
in_brick = np.loadtxt('./InsideBricks.txt', dtype=np.str)
bricknames = set(dat['brickname'])
f = open('./real_brick.txt','w')
for brick in in_brick:
    if brick in bricknames:
       f.write(brick+'\n')
f.close()
