import numpy as np
def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

def OneBrickClassify(brickname):
    log_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_new_ccd_list/logs/'+str(brickname[:3])+'/rs0/log.'+str(brickname)
    fp = open(log_dir,'r')
    string = "CCDs survive cuts"
    lines = lines_that_contain(string, fp)
    num = int(lines[-1].replace('CCDs survive cuts',''))
    f = open('BrickccdNum.txt','a')
    f.write("%s %d\n" %(brickname, num))
    return num

def BrickClassify():
    f = open('BrickccdNum.txt','w')
    f.close()
    bricks = np.loadtxt('ProcessedBricks.txt', dtype=np.str)
    for i in range(len(bricks)):
        print(bricks[i]) 
        OneBrickClassify(bricks[i])

if __name__ == '__main__':
    BrickClassify() 
