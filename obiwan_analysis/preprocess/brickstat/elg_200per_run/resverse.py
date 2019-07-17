import numpy as np
dat = np.loadtxt('UnfinishedBricks.txt',dtype = np.str)
f = open('UnfinishedBricks_reversed.txt','w')
for i in range(len(dat)):
   u=(-1)*i
   f.write(dat[u]+'\n')
f.close()

