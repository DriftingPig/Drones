from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
import numpy as np
import sys
import os
import subprocess
Nproc=25
RanFileNum=20
Type="uniform"
name = sys.argv[3]
FileDir="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/"+name+'/splitdata/'+Type+'/'
OutputELGs="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/"+name+"/BinHist/"+Type+"/" 
TotPts="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/"+name+"/BinHist/"+Type+"/TotalPoints.txt" 
if not os.path.exists(OutputELGs):
    subprocess.call(["mkdir","-p",OutputELGs])
fn1 = sys.argv[1]
fn2 = sys.argv[2]
SubFileDir=FileDir
str_data=FileDir+fn1
str_random=FileDir+fn2


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
        for i in range(0,file_num):#DD auto
            tasks.append("D%02dD%02d"%(i,i))
        for i in range(0,file_num):#DR
            for j in range(0,file_num):
                 tasks.append("D%02dR%02d"%(i,j))
        for i in range(0,file_num):#RR auto
                tasks.append("R%02dR%02d"%(i,i))
        for i in range(0,file_num):#DD cross
            for j in range(i+1,file_num): 
                tasks.append("D%02dD%02d"%(i,j))
        for i in range(0,file_num):#RR cross 
            for j in range(i+1,file_num):
                 tasks.append("R%02dR%02d"%(i,j))

        for i in range(len(tasks)):
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
    
    def data_identifier_trash(self,task):
        assert(task[0] in ['D','R'] and task[3] in ['D','R'])
        if task[1:3]==task[4:6]:
                auto=1
        else:
                auto=0

        if task[0]=='D' and task[3]=='D':
             Type=0
        elif task[0]=='R' and task[3]=='R':
             Type=2
        else:
             Type=1
        return auto,Type

    def data_identifier(self,task):
        assert(task[0] in ['D','R'] and task[3] in ['D','R'])
        if task[0]=='D' and task[3]=='D': 
             if task[1:3]==task[4:6]:
                  return 1
             else:
                  return 5
        elif task[0]=='D' and task[3]=='R':
                  return 3
        else:
             if task[1:3]==task[4:6]:
                  return 2
             else:
                  return 4

    def do_work(self, data):
        import subprocess
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        task, task_arg = data
        Type=self.data_identifier(task)
        print(Type)
        #print(["./NewData_CorrFun",str_data+task[1]+'.fits',str_data+task[3]+'.fits',str(Type),str(task[1]),str(task[3]),OutputELGs+task+'.dat',TotPts])
        print(Type,task)
        if Type==1 or Type==5:#DD
            print(["./NewData_CorrFun",str_data+str(int(task[1:3]))+'.fits',str_data+str(int(task[4:6]))+'.fits',str(Type),str(int(task[1:3])),str(int(task[4:6])),OutputELGs+task[0]+str(int(task[1:3]))+task[3]+str(int(task[4:6]))+'.dat',TotPts])
            subprocess.call(["./NewData_CorrFun",str_data+str(int(task[1:3]))+'.fits',str_data+str(int(task[4:6]))+'.fits',str(Type),str(int(task[1:3])),str(int(task[4:6])),OutputELGs+task[0]+str(int(task[1:3]))+task[3]+str(int(task[4:6]))+'.dat',TotPts])
        if Type==3:#DR
            subprocess.call(["./NewData_CorrFun",str_data+str(int(task[1:3]))+'.fits',str_random+str(int(task[4:6]))+'.fits',str(Type),str(int(task[1:3])),str(int(task[4:6])),OutputELGs+task[0]+str(int(task[1:3]))+task[3]+str(int(task[4:6]))+'.dat',TotPts])   
        if Type==2 or Type==4:#RR
            subprocess.call(["./NewData_CorrFun",str_random+str(int(task[1:3]))+'.fits',str_random+str(int(task[4:6]))+'.fits',str(Type),str(int(task[1:3])),str(int(task[4:6])),OutputELGs+task[0]+str(int(task[1:3]))+task[3]+str(int(task[4:6]))+'.dat',TotPts])
        print('  Slave %s rank %d executing "%s" task_id "%d"' % (name, rank, task, task_arg) )
        return (True, 'I completed my task (%d)' % task_arg)


def main():

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )
    
    
    
    if rank == 0: # Master
        #data_name = str_data+'0.fits'
        #subprocess.call(["./ObiwanCorr",data_name,data_name,1,0,0,OutputELGs+'D0D0.dat',TotPts])
        f = open(TotPts,'w')
        f.close()
        app = MyApp(slaves=range(1, size))
        app.run()
        app.terminate_slaves()

    else: # Any slave

        MySlave().run()

    print('Task completed (rank %d)' % (rank) )

if __name__ == "__main__":
    main()
