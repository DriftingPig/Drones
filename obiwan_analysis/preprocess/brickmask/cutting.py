import numpy as np
import argparse
import subprocess
def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description='DECaLS simulations.')
    parser.add_argument('--name_for_run',type=str,required=True)
    parser.add_argument('--chunk',type=str,required=True)
    return parser

def main():
    parser= get_parser()
    args = parser.parse_args()
    obiwan_input_fn = args.name_for_run+'_'+args.chunk+'.fits'
    obiwan_output_fn = args.name_for_run+'_'+args.chunk+'_masked.fits'
    sim_input_fn = 'sim_'+args.name_for_run+'_'+args.chunk+'.fits'
    sim_output_fn = 'sim_'+args.name_for_run+'_'+args.chunk+'_masked.fits'
    fn_maker(obiwan_input_fn, obiwan_output_fn)
    subprocess.call(["cp",'/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickmask/brickmask.conf','./'])
    subprocess.call(["/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickmask/vetomask"])
    fn_maker(sim_input_fn,sim_output_fn)
    subprocess.call(["cp",'/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickmask/brickmask.conf','./'])
    subprocess.call(["/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickmask/vetomask"])
    subprocess.call(["mv","./brickmask.conf"])

def fn_maker(fn_in,fn_out):
    with open("/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickmask/brickmask.conf", "r") as f:
       lines = f.readlines()
    in_flag = True
    out_flag = True
    with open("/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/Drones/obiwan_analysis/preprocess/brickmask/brickmask.conf", "w") as f:
         for line in lines:
            if 'INPUT' in line and in_flag:
                f.write('INPUT           = /global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'+fn_in+'\n')
                in_flag = False
            elif 'OUTPUT' in line and out_flag:
                f.write('OUTPUT          = /global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'+fn_out+'\n')
                out_flag = False
            elif 'INPUT' in line or 'OUTPUT' in line:
                continue
            else:
                f.write(line)

if __name__ == '__main__':
   main()
   #fn_maker('eBOSS_ELG_full_ALL_v4.ran.fits','eBOSS_ELG_full_ALL_v4.ran_masked.fits ')
