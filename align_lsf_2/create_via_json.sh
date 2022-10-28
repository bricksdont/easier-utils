#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

via=$base/via
csv=$base/csv

mkdir -p $via

eval "$(conda shell.bash hook)"
source activate /net/cephfs/shares/volk.cl.uzh/EASIER/WMT_Shared_Task/processing-shared-task-data/venvs/venv

python $base/align_lsf_2/srt2via.py -i $csv/align_lsf_2.csv -o $via/align_lsf_2.json
