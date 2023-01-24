#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

data=/net/cephfs/scratch/mathmu/align_lsf_2

via=$data/via
csv=$data/csv

mkdir -p $via

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

mkdir -p $via/align_lsf_2

python $base/align_lsf_2/srt2via.py -i $csv/align_lsf_2.csv -o $via/align_lsf_2

(cd $via && zip -r align_lsf_2.via_files.zip ./align_lsf_2)
