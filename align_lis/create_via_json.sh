#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

data=/scratch/mathmu/align_lis

via=$data/via
csv=$data/csv

mkdir -p $via

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

mkdir -p $via/align_lis

python $base/align_lis/srt2via.py -i $csv/align_lis.csv -o $via/align_lis

# (cd $via && zip -r align_lis.via_files.zip ./align_lis)

(cd $via && tar -czvf align_lis.via_files.tar.gz align_lis)

echo "scp mathmu@login.s3it.uzh.ch:$(realpath $via/align_lis.via_files.tar.gz)"
