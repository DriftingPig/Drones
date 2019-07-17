'''
grep CCDs\ are\ photometric /global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_like_run/logs/359/more_rs0/log.*
'''
import glob
import os
fns = glob.glob('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_ngc_run/logs/*/more_rs0/log.*')
import multiprocessing as mp
p = mp.Pool(16)
def find_mismatch(fn, string):
    fp = open(fn)
    for line in fp:
        if string in line:
             return line
    return None

print(len(fns))
def cell(fn):
    string = find_mismatch(fn, "CCDs are photometric")
    if string is not None:
       print(count)
       nums = string.replace("CCDs are photometric","").replace("of","").split()
       num1 = int(nums[0])
       num2 = int(nums[1])
       if num1!=num2:
         print('yes!'+fn+'\n')

count=0
for fn in fns:
    print(count)
    count+=1
    cell(fn)
