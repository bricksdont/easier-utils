#! /bin/bash

base=$1

data=/net/cephfs/scratch/mathmu/align_lsf_2

eval "$(conda shell.bash hook)"
source activate /net/cephfs/shares/volk.cl.uzh/EASIER/WMT_Shared_Task/processing-shared-task-data/venvs/venv

# sets variable: file_ids

. $base/align_lsf_2/define_ids.sh

for file_id in $file_ids; do

    python $base/convert_ts_to_mp4.py \
       --input $data/videos_ts/rts.$file_id.ts \
       --output $data/videos_mp4/rts.$file_id.mp4 \
       --ffmpeg-multithreaded

done
