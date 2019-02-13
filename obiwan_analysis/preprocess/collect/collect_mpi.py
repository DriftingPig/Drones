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
        #PB_fn = os.path.join(os.environ['DRONES_DIR'], 'obiwan_analysis/brickstat/FinishedBricks.txt')
        #ntasks = len(np.loadtxt(PB_fn,dtype=n.str).transpose())
        #print('total of %d tasks' % ntasks)
        #version1 end
        #version 2:
        import glob
        from astropy.table import vstack
        paths = glob.glob(os.path.join(os.environ['NGC_tractor'],'*','*'))
        final_tab = None
        n=0
        for path in paths:
            brickname = os.path.basename(path)
            self.work_queue.add_work(data=(n, brickname))   
            n+=1     
        #version 1:    
        #for i in range(ntasks):
            # 'data' will be passed to the slave and can be anything
            #self.work_queue.add_work(data=(i, i))
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
                done, tab = slave_return_data
                print('No %d is done' % done) 
                if tab is not None:
                     if final_table is not None:
                         final_table = vstack([final_table, tab])
                     else:
                         final_table = tab          
            
            # sleep some time
            time.sleep(0.3)
        print('writing all the output to one table...')
        final_table.write(os.path.join(os.environ['obiwan_out'],'subset','ngc_sim.fits'), format='fits',overwrite=True)
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
        tab = NGC_sim(task_arg)
        print('  Slave %s rank %d executing "%s" task_id "%d"' % (name, rank, task_arg, task) )
        return (task, tab)

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
