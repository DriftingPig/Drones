'''
find a few bricks that get finished with 800 randoms that has previously finished 200 randoms
'''
import os
from glob import glob
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_eight_bricks/logs/'+str(brickname[:3])+'/more_rs201/log.'+str(brickname)
    if os.path.isfile(log_dir) and "decals_sim:All done!" in open(log_dir).read():
             f = open('800_more_ProcessedBricks.txt', mode)
             f.write(str(brickname)+'\n')
             f.close()
    else:
             f = open('800_more_UnProcessedBricks.txt', mode)
             f.write(str(brickname)+'\n')
             f.close()
    

def BrickClassify():
    import numpy as np
    f1 = open('800_more_ProcessedBricks.txt', 'w')
    f1.close
    f2 = open('800_more_UnProcessedBricks.txt', 'w')
    f2.close()
    bricks = np.loadtxt('ProcessedBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')
if __name__ == '__main__':
    BrickClassify()
