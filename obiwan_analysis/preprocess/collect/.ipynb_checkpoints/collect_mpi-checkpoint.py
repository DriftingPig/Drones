from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
import numpy as np
from collect import *
from astropy.table import vstack
import os
import sys
import argparse
#should be the only thing need to be changed
BRICKPATH='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickstat/name_for_run/FinishedBricks.txt'
NAME_FOR_RUN='name4run'
class MyApp(object):
    """
    This is my application that has a lot of work to do so it gives work to do
    to its slaves until all the work is done
    """

    def __init__(self, slaves):
        # when creating taahe Master we tell it what slaves it can handle
        self.master = Master(slaves)
        # WorkQueue is a convenient class that run slaves on a tasks queue
        self.work_queue = WorkQueue(self.master)

    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        self.master.terminate_slaves()

    def run(self, name_for_run = None, split_idx = 0, N_splits = 1, tasks=None):
        """
        name for run list: elg_like_run,elg_ngc_run
        This is the core of my application, keep starting slaves
        as long as there is work to do
        """
        #
        # let's prepare our work queue. This can be built at initialization time
        # but it can also be added later as more work become available
        #
        #version 1:
        #PB_fn = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_200per_run/FinishedBricks.txt'
        #bricknames = np.loadtxt(PB_fn,dtype=n.str).transpose()
        #ntasks = len(bricknames)
        #print('total of %d tasks' % ntasks)
        #version1 end
        #version 2:
        import glob
        from astropy.table import vstack
        global BRICKPATH
        print(BRICKPATH)
        #paths = glob.glob(os.path.join(os.environ[name_for_run],'tractor','*','*'))
        #paths = np.array_split(paths, N_splits)[split_idx]
        paths = np.loadtxt(BRICKPATH,dtype=np.str)
        paths = np.array_split(paths, N_splits)[split_idx]
        final_tab = None
        final_sim = None
        n=0
        paths.sort()
        paths = paths
        for path in paths:
            brickname = os.path.basename(path)
            self.work_queue.add_work(data=(n, brickname))   
            n+=1     
        #end of verion 2
        #version 1:    
        #for i in range(ntasks):
            # 'data' will be passed to the slave and can be anything
        #    self.work_queue.add_work(data=(i, bricknames[i]))
        #version 1 end

        #
        # Keeep starting slaves as long as there is work to do
        #
        final_table = None
        sim_table = None
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
                done, tab,sim = slave_return_data
                print('No %d is done' % done) 
                if tab is not None:
                     if final_table is not None:
                         final_table = vstack((final_table, tab))
                         final_sim = vstack((final_sim,sim)) 
                     else:
                         final_table = tab          
                         final_sim=sim 
            
            # sleep some time
            time.sleep(0.3)
        print(os.environ['obiwan_out'],'subset','%s_part%d_of_%d.fits' %(name_for_run, split_idx, N_splits))
        print('writing all the output to one table...')
        final_table.write(os.path.join(os.environ['obiwan_out'],'subset','%s_part%d_of_%d.fits' % (name_for_run, split_idx, N_splits)), format='fits',overwrite=True)
        final_sim.write(os.path.join(os.environ['obiwan_out'],'subset','sim_%s_part%d_of_%d.fits' % (name_for_run, split_idx, N_splits)), format='fits',overwrite=True)
        print('done!')

class MySlave(Slave):
    """
    A slave process extends Slave class, overrides the 'do_work' method
    and calls 'Slave.run'. The Master will do the rest
    """

    def __init__(self):
        super(MySlave, self).__init__()

    def do_work(self, data):
        global NAME_FOR_RUN
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        task, task_arg = data
        #FUNCTION CAN BE CHANGED HERE
        tab,sim = production_run_general_perbrick(task_arg,env_dir=NAME_FOR_RUN, rs_type='more_rs202',region='ngc')
        print('  Slave %s rank %d executing "%s" task_id "%d"' % (name, rank, task_arg, task) )
        return (task, tab, sim)

def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description='Collection of production run data')
    parser.add_argument('--split_idx',type=int,required = True, help='index number for the chunk of bricks to stack')
    parser.add_argument('--N_split',type=int,required = True, help='total of splits for bricks')
    parser.add_argument('--name_for_run',type=str, required=True,help='production run directory (specified in DRONE_ENV.sh)')
    args = parser.parse_args(args=None)
    print(args)
    return parser

def stack(N_split, name_for_run):
    #stack data
    tab = None
    for i in range(0,N_split):
       print(fn_i)
       fn_i = os.path.join(os.environ['obiwan_out'],'subset','%s_part%d_of_%d.fits' % (name_for_run, i, N_splits))
       tab_i = Table.read(fn_i)  
       if tab is None: 
          tab = tab_i
       else:
          tab = vstack((tab, tab_i))
    print('writing')
    tab.write(os.path.join(os.environ['obiwan_out'],'subset','%s.fits') %name_for_run)
    tab = None
    for i in range(0,N_split): 
        print(fn_i)
        fn_i = os.path.join(os.environ['obiwan_out'],'subset','sim_%s_part%d_of_%d.fits' % (name_for_run, i, N_splits))  
        tab_i = Table.read(fn_i)
        if tab is None: 
           tab = tab_i
        else:
           tab = vstack((tab, tab_i))
    print('writing')
    tab.write(os.path.join(os.environ['obiwan_out'],'subset','sim_%s.fits') %name_for_run)

def main(args=None):
    if args is None:
       parser= get_parser()
       args = parser.parse_args(args=args)
    else:
       # args is already a argparse.Namespace obj
       pass
    global NAME_FOR_RUN
    global BRICKPATH
    split_idx = args.split_idx
    N_splits = args.N_split
    name_for_run = args.name_for_run
    NAME_FOR_RUN = name_for_run
    print('replacing:')
    BRICKPATH=BRICKPATH.replace('name_for_run',NAME_FOR_RUN)
    print(BRICKPATH)
    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )


    if rank == 0: # Master

        app = MyApp(slaves=range(1, size))
        app.run(split_idx = split_idx, N_splits = N_splits, name_for_run = name_for_run)
        app.terminate_slaves()

    else: # Any slave

        MySlave().run()

    print('Task completed (rank %d)' % (rank) )
    

if __name__ == "__main__":
    main()
