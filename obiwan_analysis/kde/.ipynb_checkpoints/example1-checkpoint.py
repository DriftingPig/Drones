from mpi4py import MPI
import sys
sys.path.append("../../py")
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
import numpy as np

from scipy import stats
from astropy.table import Table, hstack
from astropy.io import fits


class MyApp(object):
    """
    This is my application that has a lot of work to do so it gives work to do
    to its slaves until all the work is done
    """

    def __init__(self, slaves):
        # when creating the Master we tell it what slaves it can handle
        self.master = Master(slaves)
        # WorkQueue is a convenient class that run slaves on a tasks queue
        self.work_queue = WorkQueue(self.master)

    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        self.master.terminate_slaves()

    def run(self, tasks=None):
        """
        This is the core of my application, keep starting slaves
        as long as there is work to do
        """
        #
        # let's prepare our work queue. This can be built at initialization time
        # but it can also be added later as more work become available
        #
        task_list = np.loadtxt(BRICKSTAT_DIR + 'ProcessedBricks.txt', dtype=np.str)
        if tasks is None:
            return None
        for i in range(100):
            low = tasks[i][0]
            high = tasks[i][-1]
            # 'data' will be passed to the slave and can be anything
            self.work_queue.add_work(data=([low,high], i))
       
        #
        # Keeep starting slaves as long as there is work to do
        #
        while not self.work_queue.done():

            #
            # give more work to do to each idle slave (if any)
            #
            self.work_queue.do_work()

            #
            # reclaim returned data from completed slaves
            #
            for slave_return_data in self.work_queue.get_completed_work():
                done, message = slave_return_data
                if done:
                    print('Master: slave finished is task and says "%s"' % message)

            # sleep some time
            time.sleep(0.3)


class MySlave(Slave):
    """
    A slave process extends Slave class, overrides the 'do_work' method
    and calls 'Slave.run'. The Master will do the rest
    """

    def __init__(self):
        super(MySlave, self).__init__()

    def do_work(self, data):
        import subprocess
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        task, task_arg = data
        low,high = task[0],task[1]
        density_elg_like = kde_elg_like(values_sim[:,low:high])
        density_sim = kde_sim(values_sim[:,low:high])
        weight = density_elg_like/density_sim*(0.816040793397001/0.3785832163485753)
        tab_weight = Table(fits.BinTableHDU.from_columns(fits.ColDefs([fits.Column(name='weight',format='D',array=weight)])).data)
        tab_origin = Table(sim_contamination)[low:high]
        table_final = hstack((tab_origin,tab_weight))
        table_final.write(topdir + 'kde_outputs2/sim_kde_weighed_chunk21_part_'+str(i)+'.fits',overwrite=True)
        print('  Slave %s rank %d executing "%s" task_id "%d"' % (name, rank, task, task_arg) )
        return (True, 'I completed my task (%d)' % task_arg)


def main():
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

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )

    if rank == 0: # Master

        app = MyApp(slaves=range(1, size))
        app.run(tasks = task_list)
        app.terminate_slaves()

    else: # Any slave

        MySlave().run()

    print('Task completed (rank %d)' % (rank) )

if __name__ == "__main__":
    main()
