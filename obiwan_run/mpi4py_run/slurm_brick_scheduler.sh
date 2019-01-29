#!/bin/bash -l
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe_origin/legacypipe/py:$PYTHONPATH

RANDOMS_FROM_FITS=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat_2/brick_${1}.fits
bri=$(echo ${1} | head -c 3)
outdir=${obiwan_out}/${name_for_run}
if [ ${do_skipids} == "no" ]; then
    if [ ${do_more} == "no" ]; then
        export rsdir=rs${rowstart}
    else
        export rsdir=more_rs${rowstart}
    fi
else  
    if [ ${do_more} == "no" ]; then
       export rsdir=skip_rs${rowstart}
    else 
       export rsdir=more_skip_rs${rowstart}
    fi
fi 

log=${outdir}/logs/${bri}/${brick}/${rsdir}/log.$1
mkdir -p $(dirname $log)
echo logging to...${log}

python $obiwan_code/py/obiwan/kenobi.py --dataset ${dataset} -b $1 \
       --nobj ${nobj} --rowstart ${rowstart} -o ${object} \
       --randoms_db ${randoms_db} \
       --outdir $outdir --add_sim_noise \
       --threads $threads  \
       --do_skipids $do_skipids \
       --do_more $do_more --minid $minid \
       --randoms_from_fits $RANDOMS_FROM_FITS \
       --verbose \
       >> $log 2>&1
echo FINISHED NOW!
wait
