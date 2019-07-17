from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
import numpy as np
DR5ELGs=None
ObiwanELGs=None
OutputELGs=None
TotPts=None
#BRICKSTAT_DIR='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_ngc_run/'
#BRICKSTAT_DIR='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_like_run/'
#BRICKSTAT_DIR='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/brickstat/elg_kaylan_run/'
BRICKSTAT_DIR='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_ccds/'
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
        file_num=20
        tasks=[]
        for i in range(1,file_num):#DD auto
            tasks.append("D%dD%d"%(i,i))
        for i in range(0,file_num):#DR
            for j in range(0,file_num):
                 tasks.append("D%dR%d"%(i,j))
        for i in range(0,file_num):#RR auto
                tasks.append("R%dR%d"%(i,i))
        for i in range(0,file_num):#DD cross
            for j in range(i+1,file_num): 
                tasks.append("D%dD%d"%(i,j))
        for i in range(0,file_num):#RR cross 
            for j in range(i+1,file_num):
                 tasks.append("R%dR%d"%(i,j))

        for i in range(tasks):
            # 'data' will be passed to the slave and can be anything
            self.work_queue.add_work(data=(tasks[i], i))
       
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
    
    def data_identifier(self,task):
        if task[1]==task[3]:
                auto=1
        else:
                auto=0

        if task[0]=='D' and task[2]=='D':
             Type=0
        elif task[0]=='R' and task[2]=='R':
             Type=2
        else:
             Type=1
        return auto,Type

    def do_work(self, data):
        import subprocess
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        task, task_arg = data
        auto,Type=self.data_identifier(task)
        if Type==0:#DD
            subprocess.call(["./ObiwanCorr",DR5ELGs+task[1]+'.dat',DR5ELGs+task[3]+'.dat',auto,OutputELGs+task+'.dat',"a",Type,int(task[1]),int(task[3]),TotPts])
        if Type==1:#DR
            subprocess.call(["./ObiwanCorr",DR5ELGs+task[1]+'.dat',ObiwanELGs+task[3]+'.dat',auto,OutputELGs+task+'.dat',"a",Type,int(task[1]),int(task[3]),TotPts])   
        if Type==2:#RR
            subprocess.call(["./ObiwanCorr",ObiwanELGs+task[1]+'.dat',ObiwanELGs+task[3]+'.dat',auto,OutputELGs+task+'.dat',"a",Type,int(task[1]),int(task[3]),TotPts])
        print('  Slave %s rank %d executing "%s" task_id "%d"' % (name, rank, task, task_arg) )
        return (True, 'I completed my task (%d)' % task_arg)


def main():
    import sys
    import subprocess
    global DR5ELGs
    global ObiwanELGs
    global OutputELGs
    global TotPts
    DR5ELGs=sys.argv[1]
    ObiwanELGs=sys.argv[2]
    OutputELGs=sys.argv[3]
    TotPts=sys.argv[4]
    File_Num=20
    

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )
    
    
    
    if rank == 0: # Master

        subprocess.call(["./ObiwanCorr",DR5ELGs+'0.dat',DR5ELGs+'0.dat',1,OutputELGs+'D0D0.dat',"w",0,0,0,TotPts])
        app = MyApp(slaves=range(1, size))
        app.run()
        app.terminate_slaves()

    else: # Any slave

        MySlave().run()

    print('Task completed (rank %d)' % (rank) )

if __name__ == "__main__":
    main()
