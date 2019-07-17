import astropy.io.fits as fits
import numpy as np
import numpy as n
name_for_run='chunk21_10deg2_test'
#/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/chunk21_10deg2_test/tractor/335/3351m002/more_rs0/tractor-3351m002.fits
def get_one_brick_data(brickname):
    fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/'+name_for_run+'/tractor/'+brickname[:3]+'/'+brickname+'/more_rs0/'+'tractor-'+brickname+'.fits'
    dat = fits.getdata(fn)
    return dat

def stack_bricks():
    brick_fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickstat/chunk21_10deg2_test/FinishedBricks.txt'
    bricknames = np.loadtxt(brick_fn,dtype=np.str)
    tot=None
    for brickname in bricknames:
        print(brickname)
        tot_i = get_one_brick_data(brickname)
        flag,elg_i = select_ELG(tot_i)
        if tot is None:
            tot=elg_i
        else:
            tot = np.hstack((tot,elg_i))
    print('writing')
    return fits.BinTableHDU.from_columns(fits.ColDefs(tot)).writeto('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/10deg2.fits')


def select_ELG(dat , region = 'sgc'):
    """
    Given the path to a tractor catalog, it returns two sub catalogs with the eBOSS ELG selections applied (NGC and SGC).
    """
    # the color color selection
    g     = 22.5 - 2.5 * n.log10(dat['flux_g'] / dat['mw_transmission_g'])
    r_mag = 22.5 - 2.5 * n.log10(dat['flux_r'] / dat['mw_transmission_r'])
    z_mag = 22.5 - 2.5 * n.log10(dat['flux_z'] / dat['mw_transmission_z'])
    gr = g - r_mag
    rz = r_mag - z_mag
    color_sgc = (g>21.825)&(g<22.825)&(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.218*gr+0.571<rz)&(rz<-0.555*gr+1.901)
    color_ngc = (g>21.825)&(g<22.9)  &(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.637*gr+0.399<rz)&(rz<-0.555*gr+1.901)
    # the junk rejection criterion
    noJunk = (dat['brick_primary']) & (dat['anymask_g']==0) & (dat['anymask_r']==0) & (dat['anymask_z']==0) #& (dat['TYCHO2INBLOB']==False)
    # the low depth region rejection
    value_g=dat['psfdepth_g']
    value_r=dat['psfdepth_r']
    value_z=dat['psfdepth_z']
    gL = 62.79716079
    rL = 30.05661087
    zL_ngc = 11.0
    zL_sgc = 12.75
    depth_selection_ngc = (value_g > gL) & (value_r > rL) & (value_z > zL_ngc)
    depth_selection_sgc = (value_g > gL) & (value_r > rL) & (value_z > zL_sgc)
    # final selection boolean array :
    selection_sgc =(noJunk)&(color_sgc)&(depth_selection_sgc)
    selection_ngc =(noJunk)&(color_ngc)&(depth_selection_ngc)
    # returns the catalogs of ELGs
    if region == 'sgc':
        if len(selection_sgc.nonzero()[0])>0:
            flag = True
            return flag, dat[selection_sgc]
        else:
            flag = False
            return flag, dat[selection_sgc]
    if region == 'ngc':
            if len(selection_ngc.nonzero()[0])>0 :
                flag = True
                return flag, dat[selection_ngc]
            else:
                flag = False
                return flag, dat[selection_ngc]


stack_bricks()
