#Drones

usage manual:

brickstat: 

 location:   /global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickstat

 usage:
 python brickstat.py --name_for_run (run_name) --rs (rs type) --real_bricks_fn (all the bricks to be processed, stored in elg_real_brick_lists)

 you should make a folder here with the same run_name. This code will generate a 'FinishedBricks.txt' and a 'UnfinishedBricks.txt' in this folder. 

for processing bricks (when psfex files are not ready, generate processed bricks first. These are the bricks finishing stage_tims)

currently there's a code here: /global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickstat/elg_ngc_run/brick_preprocess.py

copy it to some other folder and run it there. It will generate 'UnprocessedBricks.txt' and 'ProcessedBricks.txt'. 
