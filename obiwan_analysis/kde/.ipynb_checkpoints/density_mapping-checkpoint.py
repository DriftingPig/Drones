import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.table import Table, hstack
from astropy.io import fits
topdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
fn_dr3_elg_like = topdir+'elg_like_contamination_chunk21.fits'
fn_sim_contamination = topdir+'sgc_run_sim_really_masked_chunk21.fits'
dr3_elg_like = fits.getdata(fn_dr3_elg_like)
sim_contamination = fits.getdata(fn_sim_contamination)
elg_like_g = 22.5 - 2.5 * np.log10(dr3_elg_like['decam_flux'].transpose()[1]/dr3_elg_like['decam_mw_transmission'].transpose()[1])
elg_like_r = 22.5 - 2.5 * np.log10(dr3_elg_like['decam_flux'].transpose()[2]/dr3_elg_like['decam_mw_transmission'].transpose()[2])
elg_like_z = 22.5 - 2.5 * np.log10(dr3_elg_like['decam_flux'].transpose()[4]/dr3_elg_like['decam_mw_transmission'].transpose()[4])
elg_like_gr = elg_like_g - elg_like_r
elg_like_rz = elg_like_r - elg_like_z
data_elg_like = np.vstack((elg_like_g, elg_like_gr, elg_like_rz))
values_elg_like = data_elg_like
kde_elg_like = stats.gaussian_kde(values_elg_like)

sim_g = 22.5 - 2.5 * np.log10(sim_contamination['gflux']/sim_contamination['mw_transmission_g'])
sim_r = 22.5 - 2.5 * np.log10(sim_contamination['rflux']/sim_contamination['mw_transmission_r'])
sim_z = 22.5 - 2.5 * np.log10(sim_contamination['zflux']/sim_contamination['mw_transmission_z'])
sim_gr = sim_g - sim_r
sim_rz = sim_r - sim_z
data_sim = np.vstack((sim_g,sim_gr,sim_rz))
values_sim = data_sim
kde_sim = stats.gaussian_kde(values_sim)

task = np.arange(len(sim_contamination))
task_list = np.array_split(task,100)
for i in range(100):
    print(i)
    low = task_list[i][0]
    high = task_list[i][-1]
    density_elg_like = kde_elg_like(values_sim[:,low:high])
    density_sim = kde_sim(values_sim[:,low:high])

    weight = density_elg_like/density_sim*(0.816040793397001/0.3785832163485753)
    tab_weight = Table(fits.BinTableHDU.from_columns(fits.ColDefs([fits.Column(name='weight',format='D',array=weight)])).data)
    tab_origin = Table(sim_contamination)[low:high]
    table_final = hstack((tab_origin,tab_weight))
    table_final.write(topdir + 'kde_outputs/sim_kde_weighed_chunk21_part_'+str(i)+'.fits',overwrite=True)
