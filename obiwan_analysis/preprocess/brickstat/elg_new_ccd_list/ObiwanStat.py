import os
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_new_ccd_list/logs/'+str(brickname[:3])+'/more_rs0/log.'+str(brickname)
    if os.path.isfile(log_dir):
        if "decals_sim:All done!" in open(log_dir).read():
            f2 = open('FinishedBricks.txt', mode)
            f2.write(str(brickname)+'\n')
            f2.close()
            return 1
    f1 = open('UnFinishedBricks.txt', mode)
    f1.write(str(brickname)+'\n')
    f1.close()
    return 2

def BrickClassify():
    import numpy as np
    f3 = open('FinishedBricks.txt', 'w')
    f3.close()
    f2 = open('UnFinishedBricks.txt', 'w')
    f3.close()
    bricks = np.loadtxt('ProcessedBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')
if __name__ == '__main__':
    BrickClassify()
