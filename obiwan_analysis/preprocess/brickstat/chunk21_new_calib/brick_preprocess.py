import os
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/chunk21_new_calib/logs/'+str(brickname[:3])+'/rs0/log.'+str(brickname)
    if os.path.isfile(log_dir) is False:
        f1 = open('UnprocessedBricks.txt', mode)
        f1.write(str(brickname)+'\n')
        f1.close()
        return -1
    flag = False
    if "Stage tims finished" in open(log_dir).read():
        f2 = open('ProcessedBricks.txt', mode)
        f2.write(str(brickname)+'\n')
        f2.close()
        return 1
    #import pdb;pdb.set_trace()
    '''
    if "NothingToDoError" in open(log_dir).read():
        f3 = open('NothingToDoError.txt', mode)
        f3.write(str(brickname)+'\n')
        f3.close()
        return 3
    '''
    f4 = open('UnprocessedBricks.txt', mode)
    f4.write(str(brickname)+'\n')
    f4.close()
    return 2

def BrickClassify():
    import numpy as np
    f1 = open('UnprocessedBricks.txt', 'w')
    f1.close
    f2 = open('ProcessedBricks.txt', 'w')
    f2.close()
    f3 = open('NothingToDoError.txt', 'w')
    f3.close()
    bricks = np.loadtxt('UnfinishedBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')
if __name__ == '__main__':
    BrickClassify()
