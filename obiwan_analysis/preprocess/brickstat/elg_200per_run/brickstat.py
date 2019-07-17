import os
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_200per_run/logs/'+str(brickname[:3])+'/more_rs0/log.'+str(brickname)
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
    bricks = np.loadtxt('InsideBrick.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')
if __name__ == '__main__':
    BrickClassify()
