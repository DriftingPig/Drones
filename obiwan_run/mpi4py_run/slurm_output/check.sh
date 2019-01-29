#!/bin/bash
log_fn=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_new_ccd_list/logs/$1/more_rs0/log.$2
grep obiwan\ start $log_fn
grep obiwan\ finshed\ at $log_fn
