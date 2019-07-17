import os
def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

def OneBrickClassify(brickname):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_new_ccd_list/logs/'+str(brickname[:3])+'/more_rs0/log.'+str(brickname)
    fp = open(log_dir,'r')
    string = "obiwan finishes in"
    if os.path.isfile(log_dir):
       lines = lines_that_contain(string, fp)
    num = lines[0].replace("obiwan finishes in","").replace("hours","")
    num = float(num)
    f = open('BrickTiming.txt','a')
    f.write("%s %f\n" %(brickname, num))
    return num

def BrickClassify():
    import numpy as np
    f1 = open('BrickTiming.txt', 'w')
    f1.close
    bricks = np.loadtxt('FinishedBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i])
        OneBrickClassify(bricks[i])
if __name__ == '__main__':
    BrickClassify()
