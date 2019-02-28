import subprocess
from file_system import * 
name ='my_ngc_run'
Type = 'uniform'
function_name = name


subprocess.call(["python","SplitFile.py",name,Type,function_name])

dirs = surveyname(name,Type)
func_name = 'dirs.'+function_name
func = eval(func_name) 
func()  
names = survey(dirs)
input1 = names.splitdata_data
input2 = names.splitdata_random
input3 = names.binhist
input4 = names.totpts

subprocess.call(['./ObiwanCorr.sh',input1,input2,input3,input4])

input1 = names.binhist_topdir
input2 = names.corr_output
subprocess.call(["python","./Corr_Plot.py",input1,input2])
print("writing output to"+str(input2))

