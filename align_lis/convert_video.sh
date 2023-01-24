#! /bin/bash

base=$1
file_id=$2

data=/scratch/mathmu/align_lis

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

mkdir -p $data/videos_mp4

python $base/convert_ts_to_mp4.py \
   --input $data/videos_ts/rts.$file_id.ts \
   --output $data/videos_mp4/rts.$file_id.mp4 \
   --ffmpeg-multithreaded
