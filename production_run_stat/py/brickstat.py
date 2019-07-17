#run this code by brickstat.py [production run name] [chunk 21/22/23/25]
import os
import sys
production_run_name = sys.argv[1]
chunk = sys.argv[2]
topdir = '../'+production_run_name+'/'
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/'+production_run_name+'/logs/'+str(brickname[:3])+'/more_rs0/log.'+str(brickname)
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
    f1 = open(topdir+'UnfinishedBricks.txt', 'w')
    f1.close
    f2 = open(topdir+'FinishedBricks.txt', 'w')
    f2.close()
    bricks = np.loadtxt(topdir+'AllNGCBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')

def BrickClassify2():
    import numpy as np
    dat_all = np.loadtxt(topdir+'AllNGCBricks.txt',dtype=np.str)
    dat_f = np.loadtxt(topdir+'FinishedBricks.txt',dtype=np.str)
    f=open(topdir+'UnFinishedBricks.txt','w')
    for brick in dat_all:
        if brick in dat_f:
           pass
        else:
           f.write('%s\n' %brick)
    f.close() 
    

if __name__ == '__main__':
    BrickClassify()
