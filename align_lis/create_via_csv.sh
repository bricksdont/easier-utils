#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

data=/scratch/mathmu/align_lis

csv=$data/csv

mkdir -p $csv

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

python $base/align_lis/create_via_csv.py --videos $data/videos_mp4 --subtitles $data/subtitles --prefix rsi > $csv/align_lis.csv
