import os
from astropy.table import Table,vstack
import numpy as np
import astropy.io.fits as fits
import glob
def briknames_kaylan():
    tractors = glob.glob(os.path.join('/global/cscratch1/sd/huikong/obiwan_Aug/HPSS/tractor/','*','*','rs0','tractor-*'))
    f = open('./kaylan_bricknames.txt','w')
    for fn in tractors:
        brickname = os.path.basename(fn).replace('tractor-','').replace('.fits','')
        f.write(brickname+'\n')
    f.close()

def bricknames_ngc():
    dat = fits.getdata('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_full_ALL_v4.dat.fits')
    bricknames = set(dat['BRICKNAME'])
    f = open('./kaylan_bricks_true.txt','w')
    kaylan_bricks = np.loadtxt('./kaylan_bricknames.txt',dtype = np.str)
    for brickname in bricknames:
       if brickname in kaylan_bricks:
          if brickname[4:5]=='p' and int(brickname[5:])>100:
              f.write(brickname+'\n')
    f.close()

def bricknames_ALL_NGC():
    dat = fits.getdata('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_full_ALL_v4.dat.fits')
    bricknames = set(dat['BRICKNAME'])
    f = open('all_ngc_bricks.txt','w')
    for brickname in bricknames:
        if brickname[4:5]=='p' and int(brickname[5:])>100:
           f.write(brickname+'\n')
    f.close()
def bricknames_extra():
    kaylan_bricks = np.loadtxt('./kaylan_bricks_true.txt',dtype=np.str)
    my_bricks = np.loadtxt('./FinishedBricks.txt',dtype=np.str)
    f = open('./bricks_extra','w')
    for brick in my_bricks:
       if brick in kaylan_bricks:
           pass
       else:
           f.write(brick+'\n')
    f.close()    

def elg_data_cut():
    fn_obiwan = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/extra_obiwan.fits'
    dat = Table.read('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_full_ALL_v4.dat.fits')
    obiwan = Table.read(fn_obiwan)
    bricknames = set(obiwan['brickname'])
    tab_data = None
    for brickname in bricknames:
        if tab_data is None:
           tab_data = dat[dat['brickname']==brickname]
           print(len(tab_data))
        else:
           tab_data = vstack((tab_data,dat[dat['brickname']==brickname]))
           print(len(tab_data))
     
    tab_data.write('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/extra_dat.fits')

def brickname_unfinished_chunk23():
    fn_chunk23 = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/eBOSS_ELG_full_ALL_v4.dat_really_masked_chunk23.fits'
    dat_chunk23 = fits.getdata(fn_chunk23)
    bricknames = set(dat_chunk23['BRICKNAME'])
    my_bricks = np.loadtxt('./FinishedBricks.txt',dtype=np.str)
    f = open('chunk23_unfinished.txt','w')
    for brickname in bricknames:
        if brickname in my_bricks:
            pass
        else:
            f.write(brickname+'\n')
    f.close()
'''
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/HPSS/tractor/logs/'+str(brickname[:3])+'/more_rs0/log.'+str(brickname)
    if os.path.isfile(log_dir) is False:
        f1 = open('UnfinishedBricks.txt', mode)
        f1.write(str(brickname)+'\n')
        f1.close()
        return -1
    flag = False
    if "decals_sim:All done!" in open(log_dir).read():
        f2 = open('FinishedBricks.txt', mode)
        f2.write(str(brickname)+'\n')
        f2.close()
        return 1
    f4 = open('UnfinishedBricks.txt', mode)
    f4.write(str(brickname)+'\n')
    f4.close()
    return 2

def BrickClassify():
    import numpy as np
    f1 = open('UnfinishedBricks.txt', 'w')
    f1.close
    f2 = open('FinishedBricks.txt', 'w')
    f2.close()
    bricks = np.loadtxt('AllNGCBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')

def BrickClassify2():
    import numpy as np
    dat_all = np.loadtxt('./AllNGCBricks.txt',dtype=np.str)
    dat_f = np.loadtxt('./FinishedBricks.txt',dtype=np.str)
    f=open('./UnFinishedBricks.txt','w')
    for brick in dat_all:
        if brick in dat_f:
           pass
        else:
           f.write('%s\n' %brick)
    f.close() 
'''    

if __name__ == '__main__':
    brickname_unfinished_chunk23()
