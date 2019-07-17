#!/bin/bash -l
#run it by: ./MultiRun.sh flilename(do not wirte dir here, write it in the FileDir)
#eg ./NewData_MultiRun.sh 'elg_240_sgc.v2.TSR.SSR.chunk21_subset' 'random-sweep.merged.chunk21_TSR_SSR_subset' 

module swap python/2.7-anaconda-5.2 python/3.6-anaconda-5.2
source activate myenv

export PYTHONPATH=.:$PYTHONPATH
Nproc=25
RanFileNum=20 #number of sub_random files

#NOTE:::file name needs to be changed every time
#$3 is run name
Type="uniform"
FileDir="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/"$3"/splitdata/"$Type"/"
OutputELGs="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out//obiwan_corr/3d/"$3"/BinHist/"$Type"/"
TotPts="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/"$3"/BinHist/"$Type"/TotalPoints.txt"
mkdir -p $OutputELGs
D="D"
R="R"
SubFileDir=$FileDir
str_data=$FileDir$1
str_random=$SubFileDir$2
strfits=".fits"
#echo $Njob
export PYTHONPATH=.:$PYTHONPATH
#for((i=1; i<=$Nproc; i++)); do
#    str5=$SubFileDir${str%.fits}${str2}${i}${str3}
#    echo $str_random $str5
#   ./SprtFile $str_random $str5 $i $Nproc
#done
function PushQue {    
Que="$Que $1"
Nrun=$(($Nrun+1))
}
function GenQue {     
OldQue=$Que
Que=""; Nrun=0
for PID in $OldQue; do
if [[ -d /proc/$PID ]]; then
PushQue $PID
fi
done
}
function ChkQue {     
OldQue=$Que
for PID in $OldQue; do
if [[ ! -d /proc/$PID ]] ; then
GenQue; break
fi
done
}
i=0
echo $str_data${i}$strfits
echo $str_data${i}$strfits

dat=".dat"
i=0
./NewData_CorrFun $str_data${i}$strfits $str_data${i}$strfits 1 0 0 ${OutputELGs}${D}$i${D}$i$dat $TotPts  #DD

for((i=1; i<$RanFileNum; i++)); do
    ./NewData_CorrFun $str_data${i}$strfits $str_data${i}$strfits 1 $i $i ${OutputELGs}${D}$i${D}$i$dat $TotPts & #DD
    PID=$!
    PushQue $PID
    while [[ $Nrun -ge $Nproc ]]; do
        ChkQue
        sleep 1
    done
done


for((i=0; i<$RanFileNum; i++)); do
    ./NewData_CorrFun $str_random${i}$strfits $str_random${i}$strfits 2 $i $i ${OutputELGs}${R}$i${R}$i$dat $TotPts  & #RR self
    PID=$!
    PushQue $PID
    while [[ $Nrun -ge $Nproc ]]; do
        ChkQue
        sleep 1
    done
done


for((i=0; i<$RanFileNum; i++)); do #DR
    for((j=0; j<$RanFileNum; j++)); do
        ./NewData_CorrFun $str_data${i}$strfits $str_random${j}$strfits 3 $i $j ${OutputELGs}${D}$i${R}$j$dat $TotPts  &
        PID=$!
        PushQue $PID
        while [[ $Nrun -ge $Nproc ]]; do
            ChkQue
            sleep 1
        done
    done
done
for((i=0; i<$RanFileNum; i++)); do #RR_cross
    for((j=i+1; j<$RanFileNum; j++)); do
            ./NewData_CorrFun $str_random${i}$strfits $str_random${j}$strfits 4 $i $j ${OutputELGs}${R}$i${R}$j$dat $TotPts &
            PID=$!
            PushQue $PID
            while [[ $Nrun -ge $Nproc ]]; do
            ChkQue
            sleep 1
            done
     done
done
for((i=0; i<$RanFileNum; i++)); do #DD_cross
    for((j=i+1; j<$RanFileNum; j++)); do
            ./NewData_CorrFun $str_data${i}$strfits $str_data${j}$strfits 5 $i $j ${OutputELGs}${D}$i${D}$j$dat $TotPts &
            PID=$!
            PushQue $PID
            while [[ $Nrun -ge $Nproc ]]; do
            ChkQue
            sleep 1
            done
     done
done
wait

echo outputs are in 
echo $OutputELGs

exit
