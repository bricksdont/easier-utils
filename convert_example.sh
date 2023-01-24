#! /bin/bash

base=$1

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

python $base/convert_ts_to_mp4.py \
   --input /shares/easier.volk.cl.uzh/WP4/spoken-to-sign_sign-to-spoken/LSF-CH/RTS/Daily_news/videos/videos_parallel/rts.2021-05-06.ts \
   --output /scratch/mathmu/align_lsf_2/t.mp4 \
   --ffmpeg-multithreaded
