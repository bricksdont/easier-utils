#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

data=/net/cephfs/scratch/mathmu/align_lsf_2

csv=$data/csv

mkdir -p $csv

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

python $base/align_lsf_2/create_via_csv.py --videos $data/videos_mp4 --subtitles $data/subtitles > $csv/align_lsf_2.csv
