'''
find a few bricks that get finished with 1000 randoms
'''
import os
from glob import glob
def OneBrickClassify(brickname,mode):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_eight_bricks/logs/'+str(brickname[:3])+'/more*/log.'+str(brickname)
    found = glob(log_dir, recursive=True)
    if len(found)>0:
       if "decals_sim:All done!" in open(found[0]).read():
             f = open('do_more_ProcessedBricks.txt', mode)
             f.write(str(brickname)+'\n')
             f.write(found[0]+'\n')
             f.close()

def BrickClassify():
    import numpy as np
    f1 = open('do_more_ProcessedBricks.txt', 'w')
    f1.close
    bricks = np.loadtxt('InsideBrick.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i],'a')
if __name__ == '__main__':
    BrickClassify()
