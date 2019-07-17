import os
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_eight_bricks/logs/'+str(brickname[:3])+'/rs0/log.'+str(brickname)
    if os.path.isfile(log_dir) is False:
        f1 = open('UnprocessedBricks.txt', mode)
        f1.write(str(brickname)+'\n')
        f1.close()
        return -1
    flag = False
    if "decals_sim:All done!" in open(log_dir).read():
        f2 = open('ProcessedBricks.txt', mode)
        f2.write(str(brickname)+'\n')
        f2.close()
        return 1
    if "BIG_BLOB_DETECTED!!" in open(log_dir).read():
          f3 = open('FailedBricks.txt',mode)
          f3.write(str(brickname)+' BIG_BLOBs\n')
          f3.close()
          return -2
    if "OSError" in open(log_dir).read(): 
        f1 = open('OSERRORBricks.txt', mode)
        f1.write(str(brickname)+'\n')
        f1.close()
        return -1
    f4 = open('UnfinishedBricks.txt', mode) 
    f4.write(str(brickname)+'\n')
    f4.close()
    return 2

def BrickClassify():
    import numpy as np
    f1 = open('UnprocessedBricks.txt', 'w')
    f1.close
    f2 = open('ProcessedBricks.txt', 'w')
    f2.close()
    f3 = open('FailedBricks.txt', 'w')
    f3.close()
    f4 = open('UnfinishedBricks.txt','w')
    f4.close()
    f5 = open('OSERRORBricks.txt', 'w')
    f5.close()
    bricks = np.loadtxt('InsideBrick.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')
    with open("OSERRORBricks.txt") as file:
        x = [l.strip() for l in file]
    f5 = open('UnprocessedBricks.txt', 'a')
    for lines in x:
      f5.write(str(lines)+'\n')
    f5.close()
if __name__ == '__main__':
    BrickClassify()
