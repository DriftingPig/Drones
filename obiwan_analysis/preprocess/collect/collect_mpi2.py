#collecting data from dr3
from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
import numpy as np
from collect import *
from astropy.table import vstack
import os
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
        #version 1:
        PB_fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_200per_run/FinishedBricks.txt'
        bricknames = np.loadtxt(PB_fn,dtype=n.str).transpose()
        bricknames.sort()
        bricknames = bricknames[0:5000]
        ntasks = len(bricknames)
        print('total of %d tasks' % ntasks)
        #version1 end
        #version 2:
        #import glob
        #from astropy.table import vstack
        #paths = glob.glob(os.path.join(os.environ['dr3_tractor_data'],'*','tractor-*.fits'))
        #final_tab = None
        #final_sim = None
        #n=0
        #for path in paths:
        #    brickname = os.path.basename(path)[8:16]
        #    self.work_queue.add_work(data=(n, brickname))   
        #    n+=1     
        #end of verion 2
        #version 1:    
        for i in range(ntasks):
            # 'data' will be passed to the slave and can be anything
            self.work_queue.add_work(data=(i, bricknames[i]))
        #version 1 end

        #
        # Keeep starting slaves as long as there is work to do
        #
        final_table = None
        tab = None
        while not self.work_queue.done():

            #
            # give more work to do to each idle slave (if any)
            #
            self.work_queue.do_work()

            #
            # reclaim returned data from completed slaves
            #
            for slave_return_data in self.work_queue.get_completed_work():
                done, flag, tab = slave_return_data
                print('No %d is done' % done) 
                if flag is True:
                     if final_table is not None:
                         final_table = vstack((final_table, tab))
                     else:
                         final_table = tab          
            
            # sleep some time
            time.sleep(0.3)
        print('writing all the output to one table...')
        final_table.write(os.path.join(os.environ['obiwan_out'],'subset','dr3_elgs.fits'), format='fits',overwrite=True)
        print('done!')

class MySlave(Slave):
    """
    A slave process extends Slave class, overrides the 'do_work' method
    and calls 'Slave.run'. The Master will do the rest
    """

    def __init__(self):
        super(MySlave, self).__init__()

    def do_work(self, data):
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        task, task_arg = data
        #FUNCTION CAN BE CHANGED HERE
        flag, tab= ELG_selection_for_dr3(task_arg,region='sgc')  
        print('  Slave %s rank %d executing "%s" task_id "%d"' % (name, rank, task_arg, task) )
        return (task, flag, tab)

def main():

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )


    if rank == 0: # Master

        app = MyApp(slaves=range(1, size))
        app.run()
        app.terminate_slaves()

    else: # Any slave

        MySlave().run()

    print('Task completed (rank %d)' % (rank) )

if __name__ == "__main__":
    main()
