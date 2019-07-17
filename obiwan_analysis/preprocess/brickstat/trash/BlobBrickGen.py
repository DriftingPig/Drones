import numpy as np
dat = np.loadtxt('FailedBricks.txt', dtype=np.str).transpose()[0]
f=open('BlobBricks.txt',"w")
for brick in dat:
    f.write(brick+'\n')
f.close()

